"""
User services with transaction safety and audit logging.
"""
import logging
import random
from datetime import timedelta
from typing import TYPE_CHECKING

from django.conf import settings
from django.core.cache import cache
from django.db import transaction
from django.utils import timezone

from varzesha.core.exceptions import ApplicationError, ValidationError
from varzesha.core.utils import model_update

from .models import BaseUser, PhoneVerificationCode, normalize_phone

if TYPE_CHECKING:
    from django.http import HttpRequest

logger = logging.getLogger("varzesha.users")


def user_create(
    *,
    phone: str,
    password: str,
    **extra_fields
) -> BaseUser:
    """
    Create a new user with phone and password.

    Args:
        phone: Iranian mobile number (normalized)
        password: User password (min 8 chars)
        **extra_fields: Additional fields (first_name, last_name, email)

    Returns:
        Created BaseUser instance

    Raises:
        ValidationError: If phone exists or password invalid
    """
    phone = normalize_phone(phone)

    # Check cache first for performance
    cache_key = f"user_exists:{phone}"
    if cache.get(cache_key):
        raise ValidationError("User with this phone number already exists.")

    if BaseUser.objects.filter(phone=phone).exists():
        cache.set(cache_key, True, 300)  # Cache 5 minutes
        raise ValidationError("User with this phone number already exists.")

    # Validate password strength
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")

    user = BaseUser(phone=phone, **extra_fields)
    user.set_password(password)
    user.full_clean()
    user.save()

    logger.info(f"User created: {user.id} ({phone})")
    return user


def user_send_verification_code(*, phone: str) -> str:
    """
    Generate and send SMS verification code with rate limiting.

    Args:
        phone: Iranian mobile number

    Returns:
        Generated 6-digit code (for testing/logging only)

    Raises:
        ValidationError: If rate limit exceeded
    """
    phone = normalize_phone(phone)

    # Rate limiting check
    rate_limit_key = f"sms_rate:{phone}"
    if cache.get(rate_limit_key):
        raise ValidationError("Please wait before requesting another code.")

    # Generate cryptographically secure code
    code = str(random.randint(100000, 999999))

    # Set expiration (5 minutes)
    expires_at = timezone.now() + timedelta(minutes=5)

    with transaction.atomic():
        # Invalidate old codes
        PhoneVerificationCode.objects.filter(
            phone=phone, is_used=False
        ).update(is_used=True)

        # Create new code
        verification = PhoneVerificationCode.objects.create(
            phone=phone,
            code=code,
            expires_at=expires_at,
        )

    # Set rate limit (60 seconds between requests)
    cache.set(rate_limit_key, True, 60)

    # Send SMS asynchronously
    from .tasks import send_sms_verification_code
    send_sms_verification_code.delay(phone, code)

    logger.info(f"SMS code sent to {phone}")
    return code


def user_verify_phone(*, phone: str, code: str) -> BaseUser:
    """
    Verify phone number with provided code.

    Args:
        phone: Iranian mobile number
        code: 6-digit verification code

    Returns:
        Verified BaseUser instance

    Raises:
        ValidationError: If code invalid, expired, or max attempts reached
        ApplicationError: If user not found
    """
    phone = normalize_phone(phone)

    try:
        verification = PhoneVerificationCode.objects.get(
            phone=phone,
            code=code,
            is_used=False,
            expires_at__gt=timezone.now(),
        )
    except PhoneVerificationCode.DoesNotExist:
        # Increment attempt on invalid code if exists
        PhoneVerificationCode.objects.filter(
            phone=phone, code=code, is_used=False
        ).update(attempt_count=models.F("attempt_count") + 1)

        raise ValidationError("Invalid or expired verification code.")

    # Check max attempts
    if verification.attempt_count >= 3:
        verification.is_used = True
        verification.save(update_fields=["is_used"])
        raise ValidationError("Too many failed attempts. Please request a new code.")

    with transaction.atomic():
        # Mark code as used
        verification.mark_used()

        # Update user
        try:
            user = BaseUser.objects.get(phone=phone)
            user.is_phone_verified = True
            user.save(update_fields=["is_phone_verified"])
        except BaseUser.DoesNotExist:
            raise ApplicationError("User not found.")

    logger.info(f"Phone verified: {user.id}")
    return user


def user_update(*, user: BaseUser, data: dict) -> BaseUser:
    """
    Update user profile fields.

    Args:
        user: User instance to update
        data: Dictionary containing fields to update

    Returns:
        Updated user instance
    """
    allowed_fields = ["first_name", "last_name", "email"]
    return model_update(instance=user, fields=allowed_fields, data=data)


def user_change_password(
    *,
    user: BaseUser,
    old_password: str,
    new_password: str
) -> BaseUser:
    """
    Change user password with validation.

    Args:
        user: User instance
        old_password: Current password
        new_password: New password (min 8 chars)

    Returns:
        Updated user instance

    Raises:
        ValidationError: If old password wrong or new password invalid
    """
    if not user.check_password(old_password):
        user.record_failed_login()
        raise ValidationError("Current password is incorrect.")

    if len(new_password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")

    if old_password == new_password:
        raise ValidationError("New password must be different from old password.")

    user.set_password(new_password)
    user.record_successful_login()  # Reset failed attempts
    user.save(update_fields=["password"])

    logger.info(f"Password changed: {user.id}")
    return user


def user_record_login(*, user: BaseUser, request: "HttpRequest | None" = None) -> None:
    """
    Record successful login with IP tracking.

    Args:
        user: User who logged in
        request: HTTP request for IP extraction
    """
    ip = None
    if request:
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")

    user.record_successful_login(ip_address=ip)
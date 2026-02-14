"""
User models with Iranian phone validation and enhanced security.
"""
import re
from typing import Self

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.utils import timezone

from varzesha.core.models import BaseModel

from .managers import BaseUserManager


def validate_iranian_phone(phone: str) -> None:
    """
    Validate Iranian mobile phone number format.

    Supports:
    - 09XXXXXXXXX (domestic)
    - +989XXXXXXXXX (international)
    - 989XXXXXXXXX (without plus)
    """
    pattern = r"^(?:\+98|0098|98|0)?9\d{9}$"
    if not re.match(pattern, phone):
        raise ValidationError(
            "Invalid Iranian phone number format. Use 09XXXXXXXXX or +989XXXXXXXXX"
        )


def normalize_phone(phone: str) -> str:
    """
    Normalize phone number to standard format (09XXXXXXXXX).

    Args:
        phone: Raw phone number input

    Returns:
        Normalized phone number starting with 0
    """
    phone = phone.strip().replace(" ", "").replace("-", "")

    if phone.startswith("+98"):
        phone = "0" + phone[3:]
    elif phone.startswith("0098"):
        phone = "0" + phone[4:]
    elif phone.startswith("98") and len(phone) == 12:
        phone = "0" + phone[2:]

    return phone


class BaseUser(BaseModel, AbstractBaseUser, PermissionsMixin):
    """
    Custom user model using Iranian phone number as primary identifier.

    Security features:
    - Phone verification required for sensitive operations
    - Password validation with minimum strength
    - Audit logging via BaseModel timestamps
    """

    phone: str = models.CharField(
        max_length=13,
        unique=True,
        validators=[validate_iranian_phone],
        db_index=True,
        help_text="Iranian mobile number (e.g., 09123456789)",
    )
    email: str = models.EmailField(blank=True, db_index=True)

    # Status flags
    is_phone_verified: bool = models.BooleanField(
        default=False,
        db_index=True,
    )
    is_verified: bool = models.BooleanField(  # ✅ ADDED: Coach verification badge (like Twitter blue checkmark)
        default=False,
        db_index=True,
        help_text="Verified coach badge",
    )
    is_active: bool = models.BooleanField(default=True)
    is_staff: bool = models.BooleanField(default=False)
    is_coach: bool = models.BooleanField(
        default=False,
        db_index=True,
    )

    # Profile info
    first_name: str = models.CharField(max_length=150, blank=True)
    last_name: str = models.CharField(max_length=150, blank=True)

    # Security tracking
    last_login_ip: str | None = models.GenericIPAddressField(
        null=True, blank=True, unpack_ipv4=True
    )
    failed_login_attempts: int = models.PositiveSmallIntegerField(default=0)
    locked_until: timezone.datetime | None = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD: str = "phone"
    REQUIRED_FIELDS: list[str] = []

    objects = BaseUserManager()

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        indexes = [
            models.Index(fields=["phone", "is_phone_verified"]),
            models.Index(fields=["is_coach", "is_verified"]),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(phone__regex=r"^0?9\d{9}$"),
                name="valid_phone_format",
                violation_error_message="Phone number must be valid Iranian format",
            ),
        ]

    def clean(self) -> None:
        """Normalize and validate phone number."""
        super().clean()
        if self.phone:
            self.phone = normalize_phone(self.phone)
            validate_iranian_phone(self.phone)

    def save(self, *args, **kwargs) -> None:
        """Ensure full validation on save."""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.phone

    @property
    def full_name(self) -> str:
        """Return full name or phone if names not set."""
        name = f"{self.first_name} {self.last_name}".strip()
        return name or self.phone

    @property
    def is_locked(self) -> bool:
        """Check if account is temporarily locked."""
        if self.locked_until and self.locked_until > timezone.now():
            return True
        return False

    def record_failed_login(self) -> None:
        """Increment failed login counter and lock if threshold reached."""
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= 5:
            self.locked_until = timezone.now() + timezone.timedelta(minutes=30)
        self.save(update_fields=["failed_login_attempts", "locked_until"])

    def record_successful_login(self, ip_address: str | None = None) -> None:
        """Reset failed attempts and record IP."""
        self.failed_login_attempts = 0
        self.locked_until = None
        if ip_address:
            self.last_login_ip = ip_address
        self.save(update_fields=["failed_login_attempts", "locked_until", "last_login_ip"])


class PhoneVerificationCode(BaseModel):
    """
    SMS verification codes with expiration and usage tracking.

    Security:
    - 5-minute expiration
    - Single-use only
    - Phone-based rate limiting via throttling
    """

    phone: str = models.CharField(max_length=13, db_index=True)
    code: str = models.CharField(max_length=6)
    is_used: bool = models.BooleanField(default=False, db_index=True)
    expires_at: timezone.datetime = models.DateTimeField(db_index=True)
    used_at: timezone.datetime | None = models.DateTimeField(null=True, blank=True)

    attempt_count: int = models.PositiveSmallIntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=["phone", "is_used", "expires_at"]),
            models.Index(fields=["expires_at"]),
        ]
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.phone}: {'USED' if self.is_used else 'ACTIVE'}"

    @property
    def is_expired(self) -> bool:
        """Check if code has expired."""
        return timezone.now() > self.expires_at

    @property
    def is_valid(self) -> bool:
        """Check if code can still be used."""
        return not self.is_used and not self.is_expired

    def mark_used(self) -> None:
        """Mark code as used with timestamp."""
        self.is_used = True
        self.used_at = timezone.now()
        self.save(update_fields=["is_used", "used_at"])

    def increment_attempt(self) -> None:
        """Track verification attempts."""
        self.attempt_count += 1
        self.save(update_fields=["attempt_count"])

        if self.attempt_count >= 3:
            self.is_used = True
            self.save(update_fields=["is_used"])
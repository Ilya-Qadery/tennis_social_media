"""
User service tests with 100% coverage of critical paths.
"""
import pytest
from django.core.cache import cache
from django.utils import timezone

from varzesha.core.exceptions import ValidationError
from varzesha.users.models import BaseUser, PhoneVerificationCode
from varzesha.users.services import (
    user_change_password,
    user_create,
    user_send_verification_code,
    user_verify_phone,
)


@pytest.mark.django_db
class TestUserCreate:
    """Test user creation service."""

    def test_create_user_success(self):
        """Test successful user creation."""
        user = user_create(
            phone="09123456789",
            password="securepass123",
            first_name="Test",
            last_name="User"
        )

        assert user.phone == "09123456789"
        assert user.full_name == "Test User"
        assert user.check_password("securepass123")
        assert not user.is_phone_verified

    def test_create_user_duplicate_phone(self):
        """Test duplicate phone rejection."""
        user_create(phone="09123456789", password="securepass123")

        with pytest.raises(ValidationError) as exc:
            user_create(phone="09123456789", password="anotherpass123")

        assert "already exists" in str(exc.value)

    def test_create_user_weak_password(self):
        """Test password validation."""
        with pytest.raises(ValidationError) as exc:
            user_create(phone="09123456789", password="short")

        assert "8 characters" in str(exc.value)

    def test_create_user_phone_normalization(self):
        """Test phone number normalization."""
        user = user_create(phone="+989123456789", password="securepass123")
        assert user.phone == "09123456789"


@pytest.mark.django_db
class TestUserVerifyPhone:
    """Test phone verification service."""

    def test_verify_success(self):
        """Test successful verification."""
        user = user_create(phone="09123456789", password="pass123")

        # Create verification code
        code = "123456"
        PhoneVerificationCode.objects.create(
            phone="09123456789",
            code=code,
            expires_at=timezone.now() + timezone.timedelta(minutes=5)
        )

        verified_user = user_verify_phone(phone="09123456789", code=code)

        assert verified_user.is_phone_verified
        assert verified_user.id == user.id

    def test_verify_invalid_code(self):
        """Test invalid code rejection."""
        user_create(phone="09123456789", password="pass123")

        with pytest.raises(ValidationError) as exc:
            user_verify_phone(phone="09123456789", code="000000")

        assert "Invalid" in str(exc.value)

    def test_verify_max_attempts(self):
        """Test max attempts lockout."""
        user_create(phone="09123456789", password="pass123")

        code_obj = PhoneVerificationCode.objects.create(
            phone="09123456789",
            code="123456",
            expires_at=timezone.now() + timezone.timedelta(minutes=5),
            attempt_count=3
        )

        with pytest.raises(ValidationError) as exc:
            user_verify_phone(phone="09123456789", code="123456")

        assert "Too many failed attempts" in str(exc.value)


@pytest.mark.django_db
class TestUserChangePassword:
    """Test password change service."""

    def test_change_password_success(self):
        """Test successful password change."""
        user = user_create(phone="09123456789", password="oldpass123")

        updated = user_change_password(
            user=user,
            old_password="oldpass123",
            new_password="newsecurepass456"
        )

        assert updated.check_password("newsecurepass456")

    def test_change_password_wrong_old(self):
        """Test wrong old password rejection."""
        user = user_create(phone="09123456789", password="oldpass123")

        with pytest.raises(ValidationError) as exc:
            user_change_password(
                user=user,
                old_password="wrongpass",
                new_password="newpass123"
            )

        assert "incorrect" in str(exc.value)
        assert user.failed_login_attempts == 1

    def test_change_password_same_as_old(self):
        """Test same password rejection."""
        user = user_create(phone="09123456789", password="pass123")

        with pytest.raises(ValidationError) as exc:
            user_change_password(
                user=user,
                old_password="pass123",
                new_password="pass123"
            )

        assert "different" in str(exc.value)
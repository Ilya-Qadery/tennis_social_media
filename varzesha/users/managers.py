from django.contrib.auth.models import BaseUserManager


class BaseUserManager(BaseUserManager):
    """Custom user manager for BaseUser model."""

    def create_user(self, phone: str, password: str = None, **extra_fields):
        """Create and save a regular user with the given phone and password."""
        if not phone:
            raise ValueError("Phone number is required")
        
        # Normalize phone
        phone = phone.strip()
        if phone.startswith("+98"):
            phone = "0" + phone[3:]
        
        user = self.model(phone=phone, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone: str, password: str = None, **extra_fields):
        """Create and save a superuser with the given phone and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_phone_verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(phone, password, **extra_fields)

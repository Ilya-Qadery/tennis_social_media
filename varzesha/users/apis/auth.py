"""
Authentication APIs with security hardening and comprehensive logging.
"""
import logging
from typing import Any

from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from varzesha.core.exceptions import ApplicationError, ValidationError
from varzesha.core.throttling import SMSRateThrottle

from ..models import normalize_phone
from ..selectors import user_get_by_phone
from ..services import (
    user_create,
    user_send_verification_code,
    user_verify_phone,
)

logger = logging.getLogger("varzesha.auth")


class UserRegisterApi(APIView):
    """
    API for user registration with phone number.

    Security:
    - Password min 8 characters
    - Phone normalization
    - Rate limiting via SMS throttle
    """

    permission_classes = []
    authentication_classes = []
    throttle_classes = [SMSRateThrottle]  # ADDED: Rate limiting

    class InputSerializer(serializers.Serializer):
        phone: str = serializers.CharField(max_length=13)
        password: str = serializers.CharField(write_only=True, min_length=8)
        first_name: str = serializers.CharField(required=False, allow_blank=True)
        last_name: str = serializers.CharField(required=False, allow_blank=True)

    class OutputSerializer(serializers.Serializer):
        id: str = serializers.UUIDField()
        phone: str = serializers.CharField()
        first_name: str = serializers.CharField()
        last_name: str = serializers.CharField()
        is_phone_verified: bool = serializers.BooleanField()

    def post(self, request: Request) -> Response:
        """Handle registration."""
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = user_create(**serializer.validated_data)
            # Send verification code
            user_send_verification_code(phone=user.phone)
        except ValidationError as e:
            logger.warning(f"Registration validation error: {e.message}")
            return Response(
                {"message": e.message, "extra": e.extra},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ApplicationError as e:
            logger.error(f"Registration application error: {e.message}")
            return Response(
                {"message": e.message, "extra": e.extra},
                status=status.HTTP_400_BAD_REQUEST
            )

        logger.info(f"User registered: {user.id}")
        return Response(
            self.OutputSerializer(user).data,
            status=status.HTTP_201_CREATED
        )


class UserSendCodeApi(APIView):
    """
    API to request SMS verification code.

    Security:
    - Rate limited: 5/hour per phone
    - User existence check
    """

    permission_classes = []
    authentication_classes = []
    throttle_classes = [SMSRateThrottle]  # ADDED: Strict rate limiting

    class InputSerializer(serializers.Serializer):
        phone: str = serializers.CharField(max_length=13)

    def post(self, request: Request) -> Response:
        """Send verification code."""
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = normalize_phone(serializer.validated_data["phone"])

        # Check if user exists
        user = user_get_by_phone(phone=phone)
        if not user:
            # Return same message to prevent user enumeration
            logger.warning(f"Send code attempt for non-existent user: {phone}")
            return Response(
                {"message": "If the phone number exists, a code has been sent."},
                status=status.HTTP_200_OK
            )

        # Check if already verified
        if user.is_phone_verified:
            return Response(
                {"message": "Phone number already verified."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user_send_verification_code(phone=phone)
        except ValidationError as e:
            return Response(
                {"message": e.message},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        return Response(
            {"message": "Verification code sent."},
            status=status.HTTP_200_OK
        )


class UserVerifyPhoneApi(APIView):
    """
    API to verify phone number with code.

    Returns JWT tokens on success for immediate login.
    """

    permission_classes = []
    authentication_classes = []

    class InputSerializer(serializers.Serializer):
        phone: str = serializers.CharField(max_length=13)
        code: str = serializers.CharField(max_length=6)

    class OutputSerializer(serializers.Serializer):
        id: str = serializers.UUIDField()
        phone: str = serializers.CharField()
        is_phone_verified: bool = serializers.BooleanField()
        access: str = serializers.CharField()
        refresh: str = serializers.CharField()

    def post(self, request: Request) -> Response:
        """Verify phone and return tokens."""
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = user_verify_phone(**serializer.validated_data)
        except ValidationError as e:
            return Response(
                {"message": e.message},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ApplicationError as e:
            return Response(
                {"message": e.message},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Generate tokens
        refresh = RefreshToken.for_user(user)

        data = {
            "id": user.id,
            "phone": user.phone,
            "is_phone_verified": user.is_phone_verified,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }

        logger.info(f"Phone verified and tokens issued: {user.id}")
        return Response(self.OutputSerializer(data).data)


class UserLoginApi(APIView):
    """
    API for user login with phone and password.

    Security:
    - Account lockout after 5 failed attempts
    - IP tracking on successful login
    """

    permission_classes = []
    authentication_classes = []

    class InputSerializer(serializers.Serializer):
        phone: str = serializers.CharField(max_length=13)
        password: str = serializers.CharField(write_only=True)

    class OutputSerializer(serializers.Serializer):
        id: str = serializers.UUIDField()
        phone: str = serializers.CharField()
        first_name: str = serializers.CharField()
        last_name: str = serializers.CharField()
        is_phone_verified: bool = serializers.BooleanField()
        is_coach: bool = serializers.BooleanField()
        access: str = serializers.CharField()
        refresh: str = serializers.CharField()

    def post(self, request: Request) -> Response:
        """Handle login."""
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = normalize_phone(serializer.validated_data["phone"])
        password = serializer.validated_data["password"]

        # Get user
        user = user_get_by_phone(phone=phone)

        # Security: Same error message for all failures to prevent enumeration
        auth_failed_response = Response(
            {"message": "Invalid phone number or password."},
            status=status.HTTP_401_UNAUTHORIZED
        )

        if not user:
            logger.warning(f"Login attempt for non-existent user: {phone}")
            return auth_failed_response

        # Check account lockout
        if user.is_locked:
            logger.warning(f"Login attempt for locked account: {user.id}")
            return Response(
                {"message": "Account temporarily locked. Please try again later."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Check password
        if not user.check_password(password):
            user.record_failed_login()
            logger.warning(f"Failed login attempt: {user.id}")
            return auth_failed_response

        # Check phone verification
        if not user.is_phone_verified:
            return Response(
                {"message": "Phone number not verified."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Record successful login
        from ..services import user_record_login
        user_record_login(user=user, request=request)

        # Generate tokens
        refresh = RefreshToken.for_user(user)

        data = {
            "id": user.id,
            "phone": user.phone,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_phone_verified": user.is_phone_verified,
            "is_coach": user.is_coach,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }

        logger.info(f"User logged in: {user.id}")
        return Response(self.OutputSerializer(data).data)
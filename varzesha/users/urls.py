"""
URL configuration for users app.
"""
from django.urls import path

from .apis.auth import (
    UserLoginApi,
    UserRegisterApi,
    UserSendCodeApi,
    UserVerifyPhoneApi,
)
from .apis.me import UserChangePasswordApi, UserMeApi

urlpatterns = [
    # Auth endpoints
    path("auth/register/", UserRegisterApi.as_view(), name="register"),
    path("auth/send-code/", UserSendCodeApi.as_view(), name="send-code"),
    path("auth/verify/", UserVerifyPhoneApi.as_view(), name="verify-phone"),
    path("auth/login/", UserLoginApi.as_view(), name="login"),
    
    # Me endpoints
    path("me/", UserMeApi.as_view(), name="me"),
    path("me/change-password/", UserChangePasswordApi.as_view(), name="change-password"),
]

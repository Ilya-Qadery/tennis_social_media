from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import BaseUser, PhoneVerificationCode


@admin.register(BaseUser)
class UserAdmin(BaseUserAdmin):
    list_display = ["phone", "full_name", "is_phone_verified", "is_coach", "is_active", "created_at"]
    list_filter = ["is_phone_verified", "is_coach", "is_active", "is_staff"]
    search_fields = ["phone", "first_name", "last_name", "email"]
    ordering = ["-created_at"]
    
    fieldsets = [
        (None, {"fields": ["phone", "password"]}),
        ("Personal info", {"fields": ["first_name", "last_name", "email"]}),
        ("Permissions", {"fields": ["is_active", "is_staff", "is_superuser", "groups", "user_permissions"]}),
        ("Status", {"fields": ["is_phone_verified", "is_coach"]}),
        ("Important dates", {"fields": ["last_login", "created_at", "updated_at"]}),
    ]
    
    add_fieldsets = [
        (None, {
            "classes": ["wide"],
            "fields": ["phone", "password1", "password2"],
        }),
    ]
    
    readonly_fields = ["created_at", "updated_at", "last_login"]


@admin.register(PhoneVerificationCode)
class PhoneVerificationCodeAdmin(admin.ModelAdmin):
    list_display = ["phone", "code", "is_used", "expires_at", "created_at"]
    list_filter = ["is_used"]
    search_fields = ["phone", "code"]
    readonly_fields = ["created_at", "updated_at"]

"""
User selectors following HackSoft style guide.
Selectors handle data fetching (read operations).
"""
from django.db.models import QuerySet

from .models import BaseUser


def user_get(*, user_id: str = None, phone: str = None) -> BaseUser:
    """
    Get a user by ID or phone number.
    
    Args:
        user_id: UUID of the user
        phone: Phone number of the user
    
    Returns:
        BaseUser instance
    
    Raises:
        BaseUser.DoesNotExist: If user not found
    """
    if user_id:
        return BaseUser.objects.get(id=user_id)
    if phone:
        return BaseUser.objects.get(phone=phone)
    raise ValueError("Either user_id or phone must be provided.")


def user_list(*, is_coach: bool = None, is_phone_verified: bool = None) -> QuerySet[BaseUser]:
    """
    Get a list of users with optional filtering.
    
    Args:
        is_coach: Filter by coach status
        is_phone_verified: Filter by phone verification status
    
    Returns:
        QuerySet of BaseUser instances
    """
    queryset = BaseUser.objects.all()
    
    if is_coach is not None:
        queryset = queryset.filter(is_coach=is_coach)
    
    if is_phone_verified is not None:
        queryset = queryset.filter(is_phone_verified=is_phone_verified)
    
    return queryset


def user_get_by_phone(*, phone: str) -> BaseUser | None:
    """
    Get a user by phone number, returns None if not found.
    
    Args:
        phone: Phone number
    
    Returns:
        BaseUser instance or None
    """
    try:
        return BaseUser.objects.get(phone=phone)
    except BaseUser.DoesNotExist:
        return None

"""
Profile selectors following HackSoft style guide.
"""
from django.db.models import QuerySet

from varzesha.users.models import BaseUser

from .models import CoachProfile, PlayerProfile


def player_profile_get(*, user_id: str = None, user: BaseUser = None) -> PlayerProfile:
    """
    Get a player profile by user ID or user instance.
    
    Args:
        user_id: UUID of the user
        user: User instance
    
    Returns:
        PlayerProfile instance
    
    Raises:
        PlayerProfile.DoesNotExist: If profile not found
    """
    if user:
        return PlayerProfile.objects.get(user=user)
    if user_id:
        return PlayerProfile.objects.get(user_id=user_id)
    raise ValueError("Either user_id or user must be provided.")


def player_profile_get_by_user(*, user: BaseUser) -> PlayerProfile | None:
    """Get player profile by user, return None if not found."""
    try:
        return PlayerProfile.objects.get(user=user)
    except PlayerProfile.DoesNotExist:
        return None


def player_profile_list(
    *,
    city: str = None,
    ntrp_min: float = None,
    ntrp_max: float = None,
    play_style: str = None,
) -> QuerySet[PlayerProfile]:
    """
    Get a list of player profiles with optional filtering.
    
    Args:
        city: Filter by city
        ntrp_min: Minimum NTRP rating
        ntrp_max: Maximum NTRP rating
        play_style: Filter by play style
    
    Returns:
        QuerySet of PlayerProfile instances
    """
    queryset = PlayerProfile.objects.select_related("user").all()
    
    if city:
        queryset = queryset.filter(city__iexact=city)
    
    if ntrp_min is not None:
        queryset = queryset.filter(ntrp_rating__gte=ntrp_min)
    
    if ntrp_max is not None:
        queryset = queryset.filter(ntrp_rating__lte=ntrp_max)
    
    if play_style:
        queryset = queryset.filter(play_style=play_style)
    
    return queryset


def coach_profile_get(*, user_id: str = None, user: BaseUser = None) -> CoachProfile:
    """
    Get a coach profile by user ID or user instance.
    
    Args:
        user_id: UUID of the user
        user: User instance
    
    Returns:
        CoachProfile instance
    """
    if user:
        return CoachProfile.objects.get(user=user)
    if user_id:
        return CoachProfile.objects.get(user_id=user_id)
    raise ValueError("Either user_id or user must be provided.")


def coach_profile_get_by_user(*, user: BaseUser) -> CoachProfile | None:
    """Get coach profile by user, return None if not found."""
    try:
        return CoachProfile.objects.get(user=user)
    except CoachProfile.DoesNotExist:
        return None


def coach_profile_list(
    *,
    city: str = None,
    is_verified: bool = None,
    min_rate: int = None,
    max_rate: int = None,
) -> QuerySet[CoachProfile]:
    """
    Get a list of coach profiles with optional filtering.
    
    Args:
        city: Filter by city
        is_verified: Filter by verification status
        min_rate: Minimum hourly rate
        max_rate: Maximum hourly rate
    
    Returns:
        QuerySet of CoachProfile instances
    """
    queryset = CoachProfile.objects.select_related("user").all()
    
    if city:
        queryset = queryset.filter(city__iexact=city)
    
    if is_verified is not None:
        queryset = queryset.filter(is_verified=is_verified)
    
    if min_rate is not None:
        queryset = queryset.filter(hourly_rate__gte=min_rate)
    
    if max_rate is not None:
        queryset = queryset.filter(hourly_rate__lte=max_rate)
    
    return queryset

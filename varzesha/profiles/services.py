"""
Profile services with atomic transactions and stats consistency.
"""
import logging
from typing import TYPE_CHECKING

from django.db import transaction

from varzesha.core.exceptions import ValidationError
from varzesha.core.utils import model_update

from .models import CoachProfile, PlayerProfile

if TYPE_CHECKING:
    from varzesha.users.models import BaseUser

logger = logging.getLogger("varzesha.profiles")


def player_profile_create(
    *,
    user: "BaseUser",
    ntrp_rating: float = 2.5,
    play_style: str | None = None,
    handedness: str | None = None,
    years_experience: int = 0,
    **extra_fields
) -> PlayerProfile:
    """
    Create player profile for user.

    Args:
        user: User to create profile for
        ntrp_rating: NTRP 1.0-7.0
        play_style: Play style preference
        handedness: Left/right/both
        years_experience: Years playing
        **extra_fields: Optional fields

    Raises:
        ValidationError: If profile already exists
    """
    if hasattr(user, "player_profile"):
        raise ValidationError("User already has a player profile.")

    profile = PlayerProfile(
        user=user,
        ntrp_rating=ntrp_rating,
        play_style=play_style or "all_court",
        handedness=handedness or "right",
        years_experience=years_experience,
        **extra_fields
    )
    profile.full_clean()
    profile.save()

    logger.info(f"Player profile created: {user.id}")
    return profile


def player_profile_update(*, profile: PlayerProfile, data: dict) -> PlayerProfile:
    """
    Update player profile fields.

    Args:
        profile: Profile to update
        data: Dictionary of fields

    Returns:
        Updated profile
    """
    allowed_fields = [
        "ntrp_rating", "play_style", "handedness", "years_experience",
        "height_cm", "weight_kg", "bio", "avatar", "city",
    ]
    return model_update(instance=profile, fields=allowed_fields, data=data)


def coach_profile_create(
    *,
    user: "BaseUser",
    certification: str = "",
    years_experience: int = 0,
    hourly_rate: int | None = None,
    **extra_fields
) -> CoachProfile:
    """
    Create coach profile and mark user as coach atomically.

    Args:
        user: User to become coach
        certification: Coach credentials
        years_experience: Years coaching
        hourly_rate: Price in Toman
        **extra_fields: Optional fields

    Raises:
        ValidationError: If already a coach
    """
    if hasattr(user, "coach_profile"):
        raise ValidationError("User already has a coach profile.")

    with transaction.atomic():
        # Update user status
        user.is_coach = True
        user.save(update_fields=["is_coach"])

        # Create profile
        profile = CoachProfile(
            user=user,
            certification=certification,
            years_experience=years_experience,
            hourly_rate=hourly_rate,
            **extra_fields
        )
        profile.full_clean()
        profile.save()

    logger.info(f"Coach profile created: {user.id}")
    return profile


def coach_profile_update(*, profile: CoachProfile, data: dict) -> CoachProfile:
    """
    Update coach profile fields.

    Args:
        profile: Profile to update
        data: Dictionary of fields

    Returns:
        Updated profile
    """
    allowed_fields = [
        "certification", "years_experience", "hourly_rate",
        "specialties", "bio", "avatar", "city", "available_days",
    ]
    return model_update(instance=profile, fields=allowed_fields, data=data)


def coach_verify(*, profile: CoachProfile) -> CoachProfile:
    """
    Verify coach profile (admin action).

    Args:
        profile: CoachProfile to verify

    Returns:
        Verified profile
    """
    profile.is_verified = True
    profile.save(update_fields=["is_verified"])
    logger.info(f"Coach verified: {profile.user.id}")
    return profile


def profile_update_stats_after_match(
    *,
    player_profile: PlayerProfile,
    won: bool
) -> PlayerProfile:
    """
    Update player stats after match completion.

    CRITICAL FIX: Added select_for_update to prevent race conditions
    when multiple matches complete simultaneously.

    Args:
        player_profile: Profile to update
        won: Whether player won the match

    Returns:
        Updated profile
    """
    with transaction.atomic():
        # Lock row to prevent race conditions
        profile = PlayerProfile.objects.select_for_update().get(
            pk=player_profile.pk
        )

        profile.matches_played += 1
        if won:
            profile.matches_won += 1

        profile.save(update_fields=["matches_played", "matches_won"])

    return profile
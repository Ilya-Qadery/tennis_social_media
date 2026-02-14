"""
Match services with atomic transactions and data consistency.
"""
from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from varzesha.core.exceptions import PermissionDeniedError, ValidationError
from varzesha.core.utils import model_update
from varzesha.profiles.services import profile_update_stats_after_match

from .models import Match, MatchInvitation, MatchStatus


def match_create(
    *,
    organizer,
    scheduled_at,
    title: str = "",
    description: str = "",
    court=None,
    court_name: str = "",
    match_type: str = "singles",
    ntrp_min: float | None = None,
    ntrp_max: float | None = None,
    is_public: bool = True,
    **extra_fields
) -> Match:
    """
    Create a new match.

    Args:
        organizer: User creating the match
        scheduled_at: Scheduled date and time (must be future)
        title: Match title
        description: Match description
        court: Court instance (optional)
        court_name: Custom court name
        match_type: singles or doubles
        ntrp_min: Minimum NTRP for opponent
        ntrp_max: Maximum NTRP for opponent
        is_public: Whether match is publicly visible
        **extra_fields: Additional fields

    Returns:
        Created Match instance

    Raises:
        ValidationError: If scheduled_at is in the past
    """
    if scheduled_at <= timezone.now():
        raise ValidationError("Match must be scheduled in the future.")

    match = Match(
        organizer=organizer,
        scheduled_at=scheduled_at,
        title=title,
        description=description,
        court=court,
        court_name=court_name,
        match_type=match_type,
        ntrp_min=ntrp_min,
        ntrp_max=ntrp_max,
        is_public=is_public,
        **extra_fields
    )
    match.full_clean()
    match.save()

    return match


def match_update(*, match: Match, user, data: dict) -> Match:
    """
    Update match fields. Only organizer can update.

    Args:
        match: Match instance to update
        user: User attempting to update
        data: Dictionary containing fields to update

    Returns:
        Updated match instance
    """
    if match.organizer != user:
        raise PermissionDeniedError("Only the organizer can update this match.")

    if match.status not in [MatchStatus.PENDING, MatchStatus.CONFIRMED]:
        raise ValidationError("Cannot update match that is not pending or confirmed.")

    # Prevent changing scheduled_at to past
    if "scheduled_at" in data and data["scheduled_at"] <= timezone.now():
        raise ValidationError("Cannot schedule match in the past.")

    allowed_fields = [
        "title", "description", "scheduled_at", "court", "court_name",
        "ntrp_min", "ntrp_max", "is_public", "duration_minutes",
    ]

    return model_update(instance=match, fields=allowed_fields, data=data)


def match_join(*, match: Match, user) -> Match:
    """
    Join a public match as opponent.

    Args:
        match: Match to join
        user: User joining the match

    Returns:
        Updated match instance
    """
    if not match.can_join:
        raise ValidationError("This match is not available to join.")

    if match.organizer == user:
        raise ValidationError("You cannot join your own match.")

    # Check NTRP compatibility if specified
    if match.ntrp_min or match.ntrp_max:
        from varzesha.profiles.selectors import player_profile_get_by_user
        profile = player_profile_get_by_user(user=user)
        if profile:
            if match.ntrp_min and profile.ntrp_rating < match.ntrp_min:
                raise ValidationError("Your NTRP rating is below the minimum required.")
            if match.ntrp_max and profile.ntrp_rating > match.ntrp_max:
                raise ValidationError("Your NTRP rating is above the maximum allowed.")

    match.opponent = user
    match.status = MatchStatus.CONFIRMED
    match.save(update_fields=["opponent", "status"])

    return match


def match_leave(*, match: Match, user) -> Match:
    """
    Leave a match as opponent.

    Args:
        match: Match to leave
        user: User leaving the match

    Returns:
        Updated match instance
    """
    if match.opponent != user:
        raise PermissionDeniedError("You are not the opponent in this match.")

    if match.status not in [MatchStatus.PENDING, MatchStatus.CONFIRMED]:
        raise ValidationError("Cannot leave match that has already started or completed.")

    match.opponent = None
    match.status = MatchStatus.PENDING
    match.save(update_fields=["opponent", "status"])

    return match


def match_cancel(*, match: Match, user, reason: str = "") -> Match:
    """
    Cancel a match.

    Args:
        match: Match to cancel
        user: User cancelling the match
        reason: Cancellation reason

    Returns:
        Updated match instance
    """
    if match.organizer != user and match.opponent != user:
        raise PermissionDeniedError("Only participants can cancel this match.")

    if match.status in [MatchStatus.COMPLETED, MatchStatus.CANCELLED]:
        raise ValidationError("Match is already completed or cancelled.")

    match.status = MatchStatus.CANCELLED
    match.cancelled_by = user
    match.cancellation_reason = reason
    match.save(update_fields=["status", "cancelled_by", "cancellation_reason"])

    return match


def match_record_score(
    *,
    match: Match,
    user,
    organizer_score: int,
    opponent_score: int,
    set_scores: list | None = None,
) -> Match:
    """
    Record match score with atomic stats update.

    CRITICAL FIX: Wrapped in transaction.atomic() to ensure match status
    and player stats are updated together. Prevents inconsistent state
    if stats update fails after match is marked completed.

    Args:
        match: Match to record score for
        user: User recording the score (must be participant)
        organizer_score: Organizer's score
        opponent_score: Opponent's score
        set_scores: Detailed set scores

    Returns:
        Updated match instance
    """
    if match.organizer != user and match.opponent != user:
        raise PermissionDeniedError("Only participants can record scores.")

    if match.status != MatchStatus.CONFIRMED:
        raise ValidationError("Match must be confirmed to record score.")

    # FIXED: Atomic transaction ensures consistency
    with transaction.atomic():
        match.organizer_score = organizer_score
        match.opponent_score = opponent_score
        if set_scores:
            match.set_scores = set_scores

        # Determine winner
        if organizer_score > opponent_score:
            match.winner = match.organizer
        elif opponent_score > organizer_score:
            match.winner = match.opponent
        # Tie: winner remains None

        match.status = MatchStatus.COMPLETED
        match.save(update_fields=[
            "organizer_score", "opponent_score", "set_scores",
            "winner", "status"
        ])

        # Update player stats (now atomic with match save)
        from varzesha.profiles.selectors import player_profile_get_by_user

        organizer_profile = player_profile_get_by_user(user=match.organizer)
        if organizer_profile:
            profile_update_stats_after_match(
                player_profile=organizer_profile,
                won=(match.winner == match.organizer)
            )

        opponent_profile = player_profile_get_by_user(user=match.opponent)
        if opponent_profile:
            profile_update_stats_after_match(
                player_profile=opponent_profile,
                won=(match.winner == match.opponent)
            )

    return match


def match_invitation_create(
    *,
    match: Match,
    invited_by,
    invited_user,
    message: str = "",
) -> MatchInvitation:
    """
    Create an invitation to join a match.

    Args:
        match: Match to invite to
        invited_by: User sending the invitation
        invited_user: User being invited
        message: Optional message

    Returns:
        Created MatchInvitation instance
    """
    if match.organizer != invited_by:
        raise PermissionDeniedError("Only the organizer can invite players.")

    if match.opponent:
        raise ValidationError("Match already has an opponent.")

    # Check for existing pending invitation
    if MatchInvitation.objects.filter(
        match=match,
        invited_user=invited_user,
        status=MatchInvitation.Status.PENDING
    ).exists():
        raise ValidationError("User already has a pending invitation to this match.")

    invitation = MatchInvitation(
        match=match,
        invited_by=invited_by,
        invited_user=invited_user,
        message=message,
    )
    invitation.full_clean()
    invitation.save()

    return invitation


def match_invitation_respond(
    *,
    invitation: MatchInvitation,
    user,
    accept: bool,
) -> Match:
    """
    Respond to a match invitation.

    Args:
        invitation: MatchInvitation to respond to
        user: User responding (must be invited_user)
        accept: Whether to accept or decline

    Returns:
        Updated Match instance
    """
    if invitation.invited_user != user:
        raise PermissionDeniedError("You are not the invited user.")

    if invitation.status != MatchInvitation.Status.PENDING:
        raise ValidationError("Invitation is no longer pending.")

    # Check if match still available
    if invitation.match.opponent:
        raise ValidationError("Match already has an opponent.")

    invitation.status = (
        MatchInvitation.Status.ACCEPTED if accept else MatchInvitation.Status.DECLINED
    )
    invitation.responded_at = timezone.now()
    invitation.save(update_fields=["status", "responded_at"])

    if accept:
        match_join(match=invitation.match, user=user)

    return invitation.match
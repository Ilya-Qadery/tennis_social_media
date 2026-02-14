"""
Match selectors following HackSoft style guide.
"""
from django.db.models import Q, QuerySet
from django.utils import timezone

from .models import Match, MatchInvitation


def match_get(*, match_id: str) -> Match:
    """
    Get a match by ID.
    
    Args:
        match_id: UUID of the match
    
    Returns:
        Match instance
    
    Raises:
        Match.DoesNotExist: If match not found
    """
    return Match.objects.select_related("organizer", "opponent", "court").get(id=match_id)


def match_list(
    *,
    user=None,
    status: str = None,
    is_public: bool = None,
    court_id: str = None,
    upcoming: bool = None,
    past: bool = None,
) -> QuerySet[Match]:
    """
    Get a list of matches with optional filtering.
    
    Args:
        user: Filter by user participation
        status: Filter by status
        is_public: Filter by visibility
        court_id: Filter by court
        upcoming: Filter for upcoming matches
        past: Filter for past matches
    
    Returns:
        QuerySet of Match instances
    """
    queryset = Match.objects.select_related("organizer", "opponent", "court").all()
    
    if user:
        queryset = queryset.filter(
            Q(organizer=user) | Q(opponent=user)
        )
    
    if status:
        queryset = queryset.filter(status=status)
    
    if is_public is not None:
        queryset = queryset.filter(is_public=is_public)
    
    if court_id:
        queryset = queryset.filter(court_id=court_id)
    
    if upcoming:
        queryset = queryset.filter(scheduled_at__gt=timezone.now())
    
    if past:
        queryset = queryset.filter(scheduled_at__lte=timezone.now())
    
    return queryset


def match_list_available(*, user) -> QuerySet[Match]:
    """
    Get list of available public matches that user can join.
    
    Args:
        user: Current user
    
    Returns:
        QuerySet of available Match instances
    """
    return Match.objects.filter(
        status="pending",
        opponent__isnull=True,
        is_public=True,
        scheduled_at__gt=timezone.now(),
    ).exclude(organizer=user).select_related("organizer", "court")


def match_invitation_get(*, invitation_id: str) -> MatchInvitation:
    """
    Get a match invitation by ID.
    
    Args:
        invitation_id: UUID of the invitation
    
    Returns:
        MatchInvitation instance
    """
    return MatchInvitation.objects.select_related("match", "invited_by", "invited_user").get(
        id=invitation_id
    )


def match_invitation_list(*, user) -> QuerySet[MatchInvitation]:
    """
    Get list of match invitations for a user.
    
    Args:
        user: User to get invitations for
    
    Returns:
        QuerySet of MatchInvitation instances
    """
    return MatchInvitation.objects.filter(
        invited_user=user,
        status="pending",
    ).select_related("match", "invited_by")


def match_get_user_stats(*, user) -> dict:
    """
    Get match statistics for a user.
    
    Args:
        user: User to get stats for
    
    Returns:
        Dictionary with statistics
    """
    total = Match.objects.filter(
        Q(organizer=user) | Q(opponent=user),
        status="completed",
    ).count()
    
    won = Match.objects.filter(winner=user).count()
    
    return {
        "total_matches": total,
        "won": won,
        "lost": total - won if total > 0 else 0,
        "win_rate": round((won / total) * 100, 1) if total > 0 else 0.0,
    }

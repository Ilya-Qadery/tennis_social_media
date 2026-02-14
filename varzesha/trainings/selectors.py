"""
Training selectors following HackSoft style guide.
"""
from django.db.models import QuerySet, Sum
from django.utils import timezone

from .models import Drill, TrainingDrill, TrainingGoal, TrainingSession


def drill_get(*, drill_id: str) -> Drill:
    """
    Get a drill by ID.
    
    Args:
        drill_id: UUID of the drill
    
    Returns:
        Drill instance
    """
    return Drill.objects.get(id=drill_id, is_public=True)


def drill_list(
    *,
    category: str = None,
    difficulty: str = None,
    created_by=None,
) -> QuerySet[Drill]:
    """
    Get a list of drills with optional filtering.
    
    Args:
        category: Filter by category
        difficulty: Filter by difficulty
        created_by: Filter by creator
    
    Returns:
        QuerySet of Drill instances
    """
    queryset = Drill.objects.filter(is_public=True)
    
    if category:
        queryset = queryset.filter(category=category)
    
    if difficulty:
        queryset = queryset.filter(difficulty=difficulty)
    
    if created_by:
        queryset = queryset.filter(created_by=created_by)
    
    return queryset


def training_session_get(*, session_id: str, user) -> TrainingSession:
    """
    Get a training session by ID. Must belong to user.
    
    Args:
        session_id: UUID of the session
        user: User requesting the session
    
    Returns:
        TrainingSession instance
    """
    return TrainingSession.objects.get(id=session_id, player=user)


def training_session_list(
    *,
    user,
    date_from=None,
    date_to=None,
) -> QuerySet[TrainingSession]:
    """
    Get a list of training sessions for a user.
    
    Args:
        user: User to get sessions for
        date_from: Filter from date
        date_to: Filter to date
    
    Returns:
        QuerySet of TrainingSession instances
    """
    queryset = TrainingSession.objects.filter(player=user).prefetch_related("drills__drill")
    
    if date_from:
        queryset = queryset.filter(date__gte=date_from)
    
    if date_to:
        queryset = queryset.filter(date__lte=date_to)
    
    return queryset


def training_session_get_stats(*, user) -> dict:
    """
    Get training statistics for a user.
    
    Args:
        user: User to get stats for
    
    Returns:
        Dictionary with statistics
    """
    sessions = TrainingSession.objects.filter(player=user)
    
    total_sessions = sessions.count()
    total_minutes = sessions.aggregate(total=Sum("duration_minutes"))["total"] or 0
    
    # This week's sessions
    from datetime import timedelta
    week_ago = timezone.now() - timedelta(days=7)
    this_week = sessions.filter(created_at__gte=week_ago).count()
    
    return {
        "total_sessions": total_sessions,
        "total_hours": round(total_minutes / 60, 1),
        "total_minutes": total_minutes,
        "this_week_sessions": this_week,
    }


def training_drill_list(*, session_id: str) -> QuerySet[TrainingDrill]:
    """
    Get drills for a specific training session.
    
    Args:
        session_id: UUID of the training session
    
    Returns:
        QuerySet of TrainingDrill instances
    """
    return TrainingDrill.objects.filter(
        training_id=session_id
    ).select_related("drill")


def training_goal_get(*, goal_id: str, user) -> TrainingGoal:
    """
    Get a training goal by ID. Must belong to user.
    
    Args:
        goal_id: UUID of the goal
        user: User requesting the goal
    
    Returns:
        TrainingGoal instance
    """
    return TrainingGoal.objects.get(id=goal_id, player=user)


def training_goal_list(*, user, status: str = None) -> QuerySet[TrainingGoal]:
    """
    Get a list of training goals for a user.
    
    Args:
        user: User to get goals for
        status: Filter by status
    
    Returns:
        QuerySet of TrainingGoal instances
    """
    queryset = TrainingGoal.objects.filter(player=user)
    
    if status:
        queryset = queryset.filter(status=status)
    
    return queryset

"""
Training services following HackSoft style guide.
"""
from django.db import transaction

from varzesha.core.exceptions import PermissionDeniedError, ValidationError
from varzesha.core.utils import model_update

from .models import Drill, TrainingDrill, TrainingGoal, TrainingSession


def drill_create(
    *,
    name: str,
    category: str,
    description: str,
    instructions: str,
    created_by=None,
    **extra_fields
) -> Drill:
    """
    Create a new drill.
    
    Args:
        name: Drill name
        category: Drill category
        description: Brief description
        instructions: Step-by-step instructions
        created_by: User creating the drill
        **extra_fields: Additional fields
    
    Returns:
        Created Drill instance
    """
    drill = Drill(
        name=name,
        category=category,
        description=description,
        instructions=instructions,
        created_by=created_by,
        **extra_fields
    )
    drill.full_clean()
    drill.save()
    return drill


def drill_update(*, drill: Drill, data: dict) -> Drill:
    """
    Update drill fields.
    
    Args:
        drill: Drill instance to update
        data: Dictionary containing fields to update
    
    Returns:
        Updated drill instance
    """
    allowed_fields = [
        "name", "category", "description", "difficulty", "duration_minutes",
        "equipment_needed", "instructions", "tips", "video_url", "image", "is_public",
    ]
    
    return model_update(instance=drill, fields=allowed_fields, data=data)


def training_session_create(
    *,
    player,
    date,
    duration_minutes: int,
    title: str = "",
    intensity: str = "medium",
    **extra_fields
) -> TrainingSession:
    """
    Create a new training session.
    
    Args:
        player: User logging the session
        date: Session date
        duration_minutes: Session duration
        title: Optional title
        intensity: Intensity level
        **extra_fields: Additional fields
    
    Returns:
        Created TrainingSession instance
    """
    session = TrainingSession(
        player=player,
        date=date,
        duration_minutes=duration_minutes,
        title=title,
        intensity=intensity,
        **extra_fields
    )
    session.full_clean()
    session.save()
    return session


def training_session_update(*, session: TrainingSession, user, data: dict) -> TrainingSession:
    """
    Update training session. Only owner can update.
    
    Args:
        session: TrainingSession instance
        user: User attempting update
        data: Dictionary containing fields to update
    
    Returns:
        Updated session instance
    """
    if session.player != user:
        raise PermissionDeniedError("Only the player can update this session.")
    
    allowed_fields = [
        "title", "date", "duration_minutes", "intensity",
        "court", "location_name", "notes", "feeling_score", "coach",
    ]
    
    return model_update(instance=session, fields=allowed_fields, data=data)


def training_session_delete(*, session: TrainingSession, user) -> None:
    """
    Delete a training session. Only owner can delete.
    
    Args:
        session: TrainingSession to delete
        user: User attempting deletion
    """
    if session.player != user:
        raise PermissionDeniedError("Only the player can delete this session.")
    
    session.delete()


def training_drill_add(
    *,
    training: TrainingSession,
    drill: Drill,
    sets: int = 1,
    reps_per_set: int = 10,
    duration_minutes: int = None,
    **extra_fields
) -> TrainingDrill:
    """
    Add a drill to a training session.
    
    Args:
        training: TrainingSession instance
        drill: Drill to add
        sets: Number of sets
        reps_per_set: Reps per set
        duration_minutes: Duration for this drill
        **extra_fields: Additional fields
    
    Returns:
        Created TrainingDrill instance
    """
    training_drill = TrainingDrill(
        training=training,
        drill=drill,
        sets=sets,
        reps_per_set=reps_per_set,
        duration_minutes=duration_minutes,
        **extra_fields
    )
    training_drill.full_clean()
    training_drill.save()
    
    # Increment drill usage count
    drill.usage_count += 1
    drill.save(update_fields=["usage_count"])
    
    return training_drill


def training_drill_update(*, training_drill: TrainingDrill, data: dict) -> TrainingDrill:
    """
    Update training drill parameters.
    
    Args:
        training_drill: TrainingDrill instance
        data: Dictionary containing fields to update
    
    Returns:
        Updated TrainingDrill instance
    """
    allowed_fields = ["sets", "reps_per_set", "duration_minutes", "success_rate", "notes"]
    
    return model_update(instance=training_drill, fields=allowed_fields, data=data)


def training_drill_remove(*, training_drill: TrainingDrill, user) -> None:
    """
    Remove a drill from a training session.
    
    Args:
        training_drill: TrainingDrill to remove
        user: User attempting removal
    """
    if training_drill.training.player != user:
        raise PermissionDeniedError("Only the player can remove drills from this session.")
    
    training_drill.delete()


def training_goal_create(
    *,
    player,
    title: str,
    target_value: int,
    start_date,
    end_date=None,
    **extra_fields
) -> TrainingGoal:
    """
    Create a training goal.
    
    Args:
        player: User setting the goal
        title: Goal title
        target_value: Target value to achieve
        start_date: Goal start date
        end_date: Goal end date (optional)
        **extra_fields: Additional fields
    
    Returns:
        Created TrainingGoal instance
    """
    goal = TrainingGoal(
        player=player,
        title=title,
        target_value=target_value,
        start_date=start_date,
        end_date=end_date,
        **extra_fields
    )
    goal.full_clean()
    goal.save()
    return goal


def training_goal_update_progress(
    *,
    goal: TrainingGoal,
    increment: int = 1,
) -> TrainingGoal:
    """
    Update goal progress.
    
    Args:
        goal: TrainingGoal instance
        increment: Amount to increment current value
    
    Returns:
        Updated TrainingGoal instance
    """
    goal.current_value += increment
    
    # Auto-complete if target reached
    if goal.current_value >= goal.target_value:
        goal.status = TrainingGoal.Status.COMPLETED
        goal.save(update_fields=["current_value", "status"])
    else:
        goal.save(update_fields=["current_value"])
    
    return goal


def training_goal_update(*, goal: TrainingGoal, user, data: dict) -> TrainingGoal:
    """
    Update training goal. Only owner can update.
    
    Args:
        goal: TrainingGoal instance
        user: User attempting update
        data: Dictionary containing fields to update
    
    Returns:
        Updated goal instance
    """
    if goal.player != user:
        raise PermissionDeniedError("Only the player can update this goal.")
    
    allowed_fields = ["title", "description", "target_value", "end_date", "status"]
    
    return model_update(instance=goal, fields=allowed_fields, data=data)

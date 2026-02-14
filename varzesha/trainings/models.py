"""
Training models with fixed validators and optimized indexing.
"""
from django.core.validators import MaxValueValidator, MinValueValidator  # FIXED: Import MaxValueValidator
from django.db import models

from varzesha.core.models import BaseModel


class DrillCategory(models.TextChoices):
    """Drill categories."""
    FOREHAND = "forehand", "Forehand"
    BACKHAND = "backhand", "Backhand"
    SERVE = "serve", "Serve"
    VOLLEY = "volley", "Volley"
    FOOTWORK = "footwork", "Footwork"
    CONDITIONING = "conditioning", "Physical Conditioning"
    STRATEGY = "strategy", "Strategy"
    WARMUP = "warmup", "Warm-up"


class DifficultyLevel(models.TextChoices):
    """Difficulty levels."""
    BEGINNER = "beginner", "Beginner"
    INTERMEDIATE = "intermediate", "Intermediate"
    ADVANCED = "advanced", "Advanced"
    PROFESSIONAL = "professional", "Professional"


class IntensityLevel(models.TextChoices):
    """Intensity levels."""
    LOW = "low", "Low"
    MEDIUM = "medium", "Medium"
    HIGH = "high", "High"
    VERY_HIGH = "very_high", "Very High"


class Drill(BaseModel):
    """
    Tennis drill/exercise library.
    """

    name: str = models.CharField(max_length=255)
    category: str = models.CharField(
        max_length=20,
        choices=DrillCategory.choices,
        default=DrillCategory.FOREHAND,
        db_index=True,  # ADDED
    )
    description: str = models.TextField()

    # Characteristics
    difficulty: str = models.CharField(
        max_length=20,
        choices=DifficultyLevel.choices,
        default=DifficultyLevel.INTERMEDIATE,
        db_index=True,  # ADDED
    )
    duration_minutes: int = models.PositiveIntegerField(
        default=15,
        help_text="Recommended duration for this drill"
    )

    # Equipment needed
    equipment_needed: list = models.JSONField(
        default=list,
        blank=True,
        help_text="List of equipment needed (e.g., ['cones', 'balls'])"
    )

    # Instructions
    instructions: str = models.TextField(
        help_text="Step-by-step instructions for the drill"
    )
    tips: str = models.TextField(
        blank=True,
        help_text="Coaching tips and common mistakes to avoid"
    )

    # Media
    video_url: str = models.URLField(blank=True)
    image = models.ImageField(upload_to="drills/%Y/%m/", blank=True)  # CHANGED: Date-based upload

    # Creator
    created_by = models.ForeignKey(
        "users.BaseUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_drills",
    )

    # Visibility
    is_public: bool = models.BooleanField(default=True, db_index=True)  # ADDED

    # Stats
    usage_count: int = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "drill"
        verbose_name_plural = "drills"
        ordering = ["category", "name"]
        indexes = [
            models.Index(fields=["category", "is_public"]),  # COMPOSITE
            models.Index(fields=["difficulty", "is_public"]),  # COMPOSITE
        ]

    def __str__(self) -> str:
        return f"{self.name} ({self.get_category_display()})"


class TrainingSession(BaseModel):
    """
    A training session logged by a player.
    """

    player = models.ForeignKey(
        "users.BaseUser",
        on_delete=models.CASCADE,
        related_name="training_sessions",
    )

    # Session details
    title: str = models.CharField(max_length=255, blank=True)
    date = models.DateField(db_index=True)  # ADDED

    # Duration
    duration_minutes: int = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Total session duration in minutes"
    )

    # Intensity
    intensity: str = models.CharField(
        max_length=20,
        choices=IntensityLevel.choices,
        default=IntensityLevel.MEDIUM,
    )

    # Location
    court = models.ForeignKey(
        "courts.Court",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="training_sessions",
    )
    location_name: str = models.CharField(max_length=255, blank=True)

    # Notes
    notes: str = models.TextField(blank=True)

    # Feeling/feedback - FIXED: MinValueValidator → MaxValueValidator
    feeling_score: int | None = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],  # FIXED
        help_text="How did you feel? 1-5"
    )

    # Coach (if supervised)
    coach = models.ForeignKey(
        "users.BaseUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="supervised_sessions",
    )

    class Meta:
        verbose_name = "training session"
        verbose_name_plural = "training sessions"
        ordering = ["-date", "-created_at"]
        indexes = [
            models.Index(fields=["player", "date"]),  # User's session history
            models.Index(fields=["date", "player"]),  # Date-based queries
        ]

    def __str__(self) -> str:
        return f"{self.player.phone} - {self.date} ({self.duration_minutes} min)"


class TrainingDrill(BaseModel):
    """
    Link between TrainingSession and Drill with specific parameters.
    """

    training = models.ForeignKey(
        TrainingSession,
        on_delete=models.CASCADE,
        related_name="drills",
    )
    drill = models.ForeignKey(
        Drill,
        on_delete=models.CASCADE,
        related_name="training_instances",
    )

    # Session-specific parameters
    sets: int = models.PositiveIntegerField(default=1)
    reps_per_set: int = models.PositiveIntegerField(default=10)
    duration_minutes: int | None = models.PositiveIntegerField(null=True, blank=True)

    # Performance tracking - FIXED: MinValueValidator → MaxValueValidator
    success_rate: int | None = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],  # FIXED
        help_text="Success rate percentage"
    )
    notes: str = models.TextField(blank=True)

    class Meta:
        verbose_name = "training drill"
        verbose_name_plural = "training drills"
        ordering = ["created_at"]

    def __str__(self) -> str:
        return f"{self.drill.name} in {self.training.date}"


class TrainingGoal(BaseModel):
    """
    Player training goals.
    """

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        COMPLETED = "completed", "Completed"
        ABANDONED = "abandoned", "Abandoned"

    player = models.ForeignKey(
        "users.BaseUser",
        on_delete=models.CASCADE,
        related_name="training_goals",
    )

    title: str = models.CharField(max_length=255)
    description: str = models.TextField(blank=True)

    # Target
    target_value: int = models.PositiveIntegerField(
        help_text="Target value (e.g., 10 sessions, 1000 serves)"
    )
    current_value: int = models.PositiveIntegerField(default=0)

    # Timeframe
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    # Status
    status: str = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
        db_index=True,  # ADDED
    )

    class Meta:
        verbose_name = "training goal"
        verbose_name_plural = "training goals"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["player", "status"]),  # ADDED: Active goals lookup
        ]

    def __str__(self) -> str:
        return f"{self.player.phone} - {self.title}"

    @property
    def progress_percentage(self) -> int:
        if self.target_value == 0:
            return 0
        return min(100, int((self.current_value / self.target_value) * 100))
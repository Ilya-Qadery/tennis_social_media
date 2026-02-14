"""
Match models with atomic operations and business logic constraints.
"""
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone  # ADDED
from django.core.exceptions import ValidationError

from varzesha.core.models import BaseModel


class MatchStatus(models.TextChoices):
    """Match status choices."""
    PENDING = "pending", "Pending"
    CONFIRMED = "confirmed", "Confirmed"
    IN_PROGRESS = "in_progress", "In Progress"
    COMPLETED = "completed", "Completed"
    CANCELLED = "cancelled", "Cancelled"
    NO_SHOW = "no_show", "No Show"


class MatchType(models.TextChoices):
    """Match type choices."""
    SINGLES = "singles", "Singles"
    DOUBLES = "doubles", "Doubles"


class Match(BaseModel):
    """
    Tennis match model with scheduling and scoring.
    """

    # Organizer (creator of the match)
    organizer = models.ForeignKey(
        "users.BaseUser",
        on_delete=models.CASCADE,
        related_name="organized_matches",
    )

    # Opponent (can be null initially - looking for opponent)
    opponent = models.ForeignKey(
        "users.BaseUser",
        on_delete=models.CASCADE,
        related_name="matches",
        null=True,
        blank=True,
    )

    # Match details
    title: str = models.CharField(max_length=255, blank=True)
    description: str = models.TextField(blank=True)

    # Type
    match_type: str = models.CharField(
        max_length=10,
        choices=MatchType.choices,
        default=MatchType.SINGLES,
        db_index=True,  # ADDED
    )

    # Scheduling
    scheduled_at = models.DateTimeField(db_index=True)  # ADDED
    duration_minutes: int = models.PositiveIntegerField(
        default=90,
        help_text="Expected duration in minutes"
    )

    # Location
    court = models.ForeignKey(
        "courts.Court",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="matches",
    )
    court_name: str = models.CharField(
        max_length=255,
        blank=True,
        help_text="Custom court name if not using registered court"
    )

    # Status
    status: str = models.CharField(
        max_length=20,
        choices=MatchStatus.choices,
        default=MatchStatus.PENDING,
        db_index=True,  # ADDED
    )

    # Scoring
    organizer_score: int | None = models.PositiveIntegerField(null=True, blank=True)
    opponent_score: int | None = models.PositiveIntegerField(null=True, blank=True)

    # Set scores (JSON for flexibility)
    set_scores: list = models.JSONField(
        default=list,
        blank=True,
        help_text="List of sets: [[6,4], [3,6], [6,2]]"
    )

    # Winner
    winner = models.ForeignKey(
        "users.BaseUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="won_matches",
    )

    # Match preferences
    ntrp_min: float | None = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        null=True,
        blank=True,
        validators=[MinValueValidator(1.0)],
        help_text="Minimum NTRP rating for opponent"
    )
    ntrp_max: float | None = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        null=True,
        blank=True,
        validators=[MinValueValidator(1.0)],
        help_text="Maximum NTRP rating for opponent"
    )

    # Visibility
    is_public: bool = models.BooleanField(
        default=True,
        help_text="Public matches are visible to all players",
        db_index=True,  # ADDED
    )

    # Cancellation
    cancelled_by = models.ForeignKey(
        "users.BaseUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cancelled_matches",
    )
    cancellation_reason: str = models.TextField(blank=True)

    class Meta:
        verbose_name = "match"
        verbose_name_plural = "matches"
        ordering = ["-scheduled_at"]
        indexes = [
            models.Index(fields=["organizer", "status"]),
            models.Index(fields=["opponent", "status"]),
            models.Index(fields=["scheduled_at", "status"]),  # COMPOSITE
            models.Index(fields=["status", "is_public", "scheduled_at"]),  # COMPOSITE for available matches
            models.Index(fields=["court"]),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(ntrp_min__isnull=True) | models.Q(ntrp_max__isnull=True) | models.Q(
                    ntrp_min__lte=models.F("ntrp_max")),
                name="valid_ntrp_range",
                violation_error_message="NTRP min must be less than or equal to NTRP max",
            ),
        ]

    def __str__(self) -> str:
        opponent_str = self.opponent.phone if self.opponent else "TBD"
        return f"{self.organizer.phone} vs {opponent_str} - {self.status}"

    @property
    def is_completed(self) -> bool:
        return self.status == MatchStatus.COMPLETED

    @property
    def can_join(self) -> bool:
        """
        FIXED: Added future date check to prevent joining past matches.
        """
        return (
                self.status == MatchStatus.PENDING
                and self.opponent is None
                and self.is_public
                and self.scheduled_at > timezone.now()  # FIXED: Must be in future
        )

    def clean(self) -> None:
        """Validate match data."""
        super().clean()
        if self.scheduled_at and self.scheduled_at < timezone.now():
            # Only validate on creation, allow past dates for historical records
            if self._state.adding:
                raise ValidationError("Match must be scheduled in the future.")


class MatchInvitation(BaseModel):
    """
    Invitation to join a match.
    """

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        ACCEPTED = "accepted", "Accepted"
        DECLINED = "declined", "Declined"
        EXPIRED = "expired", "Expired"

    match = models.ForeignKey(
        Match,
        on_delete=models.CASCADE,
        related_name="invitations",
    )
    invited_by = models.ForeignKey(
        "users.BaseUser",
        on_delete=models.CASCADE,
        related_name="sent_invitations",
    )
    invited_user = models.ForeignKey(
        "users.BaseUser",
        on_delete=models.CASCADE,
        related_name="received_invitations",
    )
    status: str = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,  # ADDED
    )
    message: str = models.TextField(blank=True)
    responded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "match invitation"
        verbose_name_plural = "match invitations"
        unique_together = ["match", "invited_user"]
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["invited_user", "status"]),  # ADDED: Pending invites lookup
        ]

    def __str__(self) -> str:
        return f"{self.invited_by.phone} invited {self.invited_user.phone} to match"


class MatchComment(BaseModel):
    """
    Comments on matches.
    """

    match = models.ForeignKey(
        Match,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    user = models.ForeignKey(
        "users.BaseUser",
        on_delete=models.CASCADE,
        related_name="match_comments",
    )
    content: str = models.TextField()

    class Meta:
        verbose_name = "match comment"
        verbose_name_plural = "match comments"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.user.phone} on match {self.match.id}"
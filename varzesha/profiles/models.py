from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from varzesha.core.models import BaseModel


class PlayStyle(models.TextChoices):
    """Tennis play styles."""
    BASELINE = "baseline", "Baseline Player"
    SERVE_VOLLEY = "serve_volley", "Serve and Volley"
    ALL_COURT = "all_court", "All Court Player"
    COUNTER_PUNCHER = "counter_puncher", "Counter Puncher"


class Handedness(models.TextChoices):
    """Player handedness."""
    RIGHT = "right", "Right-handed"
    LEFT = "left", "Left-handed"
    BOTH = "both", "Ambidextrous"


class PlayerProfile(BaseModel):
    """
    Extended profile for tennis players.
    """
    
    user = models.OneToOneField(
        "users.BaseUser",
        on_delete=models.CASCADE,
        related_name="player_profile",
    )
    
    # NTRP Rating (1.0 - 7.0)
    ntrp_rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=2.5,
        validators=[
            MinValueValidator(1.0),
            MaxValueValidator(7.0),
        ],
        help_text="NTRP rating from 1.0 (beginner) to 7.0 (pro)",
    )
    
    # Playing characteristics
    play_style = models.CharField(
        max_length=20,
        choices=PlayStyle.choices,
        default=PlayStyle.ALL_COURT,
    )
    handedness = models.CharField(
        max_length=10,
        choices=Handedness.choices,
        default=Handedness.RIGHT,
    )
    
    # Experience
    years_experience = models.PositiveIntegerField(default=0)
    
    # Physical
    height_cm = models.PositiveIntegerField(null=True, blank=True)
    weight_kg = models.PositiveIntegerField(null=True, blank=True)
    
    # Bio
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/players/", blank=True)
    
    # Location
    city = models.CharField(max_length=100, blank=True)
    
    # Stats
    matches_played = models.PositiveIntegerField(default=0)
    matches_won = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = "player profile"
        verbose_name_plural = "player profiles"
        indexes = [
            models.Index(fields=["ntrp_rating"]),
            models.Index(fields=["city"]),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(ntrp_rating__gte=1.0, ntrp_rating__lte=7.0),
                name="valid_ntrp_rating",
            ),
        ]
    
    def __str__(self):
        return f"{self.user.phone} - NTRP {self.ntrp_rating}"
    
    @property
    def win_rate(self) -> float:
        if self.matches_played == 0:
            return 0.0
        return round((self.matches_won / self.matches_played) * 100, 1)


class CoachProfile(BaseModel):
    """
    Extended profile for tennis coaches.
    """
    
    user = models.OneToOneField(
        "users.BaseUser",
        on_delete=models.CASCADE,
        related_name="coach_profile",
    )
    
    # Verification
    is_verified = models.BooleanField(default=False)
    
    # Professional info
    certification = models.CharField(max_length=255, blank=True)
    years_experience = models.PositiveIntegerField(default=0)
    
    # Pricing (in Toman)
    hourly_rate = models.PositiveIntegerField(null=True, blank=True)
    
    # Specialties
    specialties = models.JSONField(default=list, blank=True)
    
    # Bio
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/coaches/", blank=True)
    
    # Location
    city = models.CharField(max_length=100, blank=True)
    
    # Availability
    available_days = models.JSONField(default=list, blank=True)
    
    # Stats
    total_students = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
    )
    
    class Meta:
        verbose_name = "coach profile"
        verbose_name_plural = "coach profiles"
        indexes = [
            models.Index(fields=["is_verified"]),
            models.Index(fields=["city"]),
            models.Index(fields=["hourly_rate"]),
        ]
    
    def __str__(self):
        return f"Coach {self.user.phone} - {'Verified' if self.is_verified else 'Unverified'}"

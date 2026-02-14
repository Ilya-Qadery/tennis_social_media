"""
Court models with optimized indexing and rating system.
"""
from django.contrib.postgres.indexes import GinIndex  # ADDED: Full-text search
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models, transaction
from django.db.models import Avg, Count
from django.core.exceptions import ValidationError

from varzesha.core.models import BaseModel


class SurfaceType(models.TextChoices):
    """Tennis court surface types."""
    HARD = "hard", "Hard Court"
    CLAY = "clay", "Clay Court"
    GRASS = "grass", "Grass Court"
    CARPET = "carpet", "Carpet Court"
    ARTIFICIAL = "artificial", "Artificial Grass"


class Court(BaseModel):
    """
    Tennis court model with optimized querying and automatic rating updates.

    Indexes:
    - city + is_active: Location filtering
    - surface_type: Surface filtering  
    - price_per_hour: Price range queries
    - average_rating: Rating sorting
    - location_gin: Full-text search on name/address
    """

    name: str = models.CharField(max_length=255)
    description: str = models.TextField(blank=True)

    # Location
    city: str = models.CharField(max_length=100, db_index=True)
    address: str = models.TextField()
    lat: float | None = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
    )
    lng: float | None = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
    )

    # Characteristics
    surface_type: str = models.CharField(
        max_length=20,
        choices=SurfaceType.choices,
        default=SurfaceType.HARD,
        db_index=True,  # ADDED
    )
    indoor: bool = models.BooleanField(default=False, db_index=True)  # ADDED
    has_lights: bool = models.BooleanField(default=False, db_index=True)  # ADDED

    # Pricing (Toman)
    price_per_hour: int = models.PositiveIntegerField(
        db_index=True,  # ADDED
        help_text="Price per hour in Iranian Toman"
    )

    # Facilities
    has_parking: bool = models.BooleanField(default=False, db_index=True)  # ADDED
    has_showers: bool = models.BooleanField(default=False, db_index=True)  # ADDED
    has_locker_room: bool = models.BooleanField(default=False)
    has_equipment_rental: bool = models.BooleanField(default=False)

    # Contact
    phone: str = models.CharField(max_length=13, blank=True)
    website: str = models.URLField(blank=True)

    # Status
    is_active: bool = models.BooleanField(default=True, db_index=True)  # ADDED

    # Images
    main_image = models.ImageField(upload_to="courts/%Y/%m/", blank=True)

    # Stats (denormalized for performance)
    total_ratings: int = models.PositiveIntegerField(default=0)
    average_rating: float = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
    )

    class Meta:
        verbose_name = "court"
        verbose_name_plural = "courts"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["city", "is_active"]),
            models.Index(fields=["surface_type", "is_active"]),  # COMPOSITE
            models.Index(fields=["price_per_hour", "is_active"]),  # COMPOSITE
            models.Index(fields=["average_rating", "is_active"]),  # COMPOSITE
            GinIndex(  # ADDED: Full-text search
                name="court_search_gin",
                fields=["name", "address", "city"],
                opclasses=["gin_trgm_ops", "gin_trgm_ops", "gin_trgm_ops"],
            ),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(price_per_hour__gte=0),
                name="positive_price",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.name} - {self.city}"

    def update_rating(self) -> None:
        """
        Recalculate average rating from reviews.

        CRITICAL FIX: This method was missing in original code.
        Called by CourtReview.save() signal.
        """
        with transaction.atomic():
            # Lock row to prevent race conditions
            court = Court.objects.select_for_update().get(pk=self.pk)

            stats = court.reviews.aggregate(
                avg=Avg("rating"),
                count=Count("id")
            )

            court.average_rating = stats["avg"] or 0.0
            court.total_ratings = stats["count"]
            court.save(update_fields=["average_rating", "total_ratings"])

    @property
    def location_dict(self) -> dict[str, float | None]:
        """Return location as dictionary for API serialization."""
        return {
            "lat": float(self.lat) if self.lat else None,
            "lng": float(self.lng) if self.lng else None,
        }


class CourtReview(BaseModel):
    """
    User reviews for courts with automatic rating updates.

    Constraints:
    - One review per user per court
    - Rating 1-5
    """

    court: Court = models.ForeignKey(
        Court,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    user = models.ForeignKey(
        "users.BaseUser",
        on_delete=models.CASCADE,
        related_name="court_reviews",
    )
    rating: int = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    comment: str = models.TextField(blank=True)

    class Meta:
        verbose_name = "court review"
        verbose_name_plural = "court reviews"
        unique_together = ["court", "user"]
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["court", "created_at"]),  # ADDED: Review listing
        ]

    def __str__(self) -> str:
        return f"{self.user.phone} - {self.court.name} ({self.rating}/5)"

    def save(self, *args, **kwargs) -> None:
        """Save review and trigger rating update."""
        super().save(*args, **kwargs)
        # Update court's average rating
        self.court.update_rating()

    def delete(self, *args, **kwargs) -> None:
        """Delete review and update rating."""
        court = self.court
        super().delete(*args, **kwargs)
        court.update_rating()


class CourtAvailability(BaseModel):
    """
    Court availability time slots.

    Validation: start_time < end_time enforced in clean()
    """

    DAYS_OF_WEEK = [
        (0, "Monday"),
        (1, "Tuesday"),
        (2, "Wednesday"),
        (3, "Thursday"),
        (4, "Friday"),
        (5, "Saturday"),
        (6, "Sunday"),
    ]

    court: Court = models.ForeignKey(
        Court,
        on_delete=models.CASCADE,
        related_name="availabilities",
    )
    day_of_week: int = models.PositiveSmallIntegerField(
        choices=DAYS_OF_WEEK,
        validators=[MinValueValidator(0), MaxValueValidator(6)],
    )
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available: bool = models.BooleanField(default=True, db_index=True)  # ADDED

    class Meta:
        verbose_name = "court availability"
        verbose_name_plural = "court availabilities"
        ordering = ["day_of_week", "start_time"]
        indexes = [
            models.Index(fields=["court", "day_of_week", "is_available"]),  # COMPOSITE
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(start_time__lt=models.F("end_time")),
                name="valid_time_range",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.court.name} - {self.get_day_of_week_display()} {self.start_time}-{self.end_time}"

    def clean(self) -> None:
        """Validate time range."""
        if self.start_time >= self.end_time:
            raise ValidationError("Start time must be before end time.")
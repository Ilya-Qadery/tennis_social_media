"""
Court services with transaction safety and cache invalidation.
"""
from django.core.cache import cache
from django.db import transaction

from varzesha.core.exceptions import ValidationError
from varzesha.core.utils import model_update

from .models import Court, CourtAvailability, CourtReview


def court_create(
    *,
    name: str,
    city: str,
    address: str,
    price_per_hour: int,
    **extra_fields
) -> Court:
    """
    Create a new tennis court.

    Args:
        name: Court name
        city: City name
        address: Full address
        price_per_hour: Price in Toman (must be > 0)
        **extra_fields: Optional fields

    Returns:
        Created Court instance

    Raises:
        ValidationError: If validation fails
    """
    if price_per_hour <= 0:
        raise ValidationError("Price must be greater than 0.")

    court = Court(
        name=name,
        city=city,
        address=address,
        price_per_hour=price_per_hour,
        **extra_fields
    )
    court.full_clean()
    court.save()

    # Invalidate cities cache
    cache.delete("court_cities")

    return court


def court_update(*, court: Court, data: dict) -> Court:
    """
    Update court fields with cache invalidation.

    Args:
        court: Court instance to update
        data: Dictionary of fields to update

    Returns:
        Updated court instance
    """
    allowed_fields = [
        "name", "description", "city", "address", "lat", "lng",
        "surface_type", "indoor", "has_lights", "price_per_hour",
        "has_parking", "has_showers", "has_locker_room", "has_equipment_rental",
        "phone", "website", "is_active", "main_image",
    ]

    old_city = court.city
    court = model_update(instance=court, fields=allowed_fields, data=data)

    # Invalidate caches if city changed
    if "city" in data and data["city"] != old_city:
        cache.delete("court_cities")

    # Invalidate court cache
    cache.delete(f"court:{court.id}")

    return court


def court_review_create(
    *,
    court: Court,
    user,
    rating: int,
    comment: str = ""
) -> CourtReview:
    """
    Create a review for a court.

    Args:
        court: Court being reviewed
        user: User creating review
        rating: 1-5 rating
        comment: Optional text comment

    Returns:
        Created CourtReview

    Raises:
        ValidationError: If user already reviewed this court
    """
    # Check for existing review (atomic to prevent race)
    with transaction.atomic():
        existing = CourtReview.objects.filter(
            court=court,
            user=user
        ).select_for_update(nowait=False).first()

        if existing:
            raise ValidationError("You have already reviewed this court.")

        review = CourtReview(
            court=court,
            user=user,
            rating=rating,
            comment=comment,
        )
        review.full_clean()
        review.save()  # Triggers court.update_rating() via signal

    # Invalidate court cache
    cache.delete(f"court:{court.id}")

    return review


def court_review_update(*, review: CourtReview, data: dict) -> CourtReview:
    """
    Update a court review.

    Args:
        review: CourtReview to update
        data: Dictionary with rating and/or comment

    Returns:
        Updated review
    """
    allowed_fields = ["rating", "comment"]
    review = model_update(instance=review, fields=allowed_fields, data=data)

    # Trigger rating recalculation if rating changed
    if "rating" in data:
        review.court.update_rating()
        cache.delete(f"court:{review.court.id}")

    return review


def court_availability_create(
    *,
    court: Court,
    day_of_week: int,
    start_time,
    end_time,
    is_available: bool = True,
) -> CourtAvailability:
    """
    Create availability slot for a court.

    Args:
        court: Court instance
        day_of_week: 0=Monday, 6=Sunday
        start_time: Opening time
        end_time: Closing time
        is_available: Whether slot is bookable

    Returns:
        Created CourtAvailability
    """
    availability = CourtAvailability(
        court=court,
        day_of_week=day_of_week,
        start_time=start_time,
        end_time=end_time,
        is_available=is_available,
    )
    availability.full_clean()
    availability.save()
    return availability
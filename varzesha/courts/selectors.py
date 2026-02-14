"""
Court selectors with query optimization and caching.
"""
from django.db.models import Avg, QuerySet
from django.core.cache import cache
from django.db import models

from .models import Court, CourtReview


def court_get(*, court_id: str) -> Court:
    """
    Get a court by ID with related data prefetch.

    Args:
        court_id: UUID of the court

    Returns:
        Court instance with prefetched reviews

    Raises:
        Court.DoesNotExist: If court not found or inactive
    """
    cache_key = f"court:{court_id}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    try:
        court = Court.objects.select_related().get(
            id=court_id,
            is_active=True
        )
        cache.set(cache_key, court, 300)  # 5 minutes
        return court
    except Court.DoesNotExist:
        raise


def court_list(
    *,
    city: str | None = None,
    surface_type: str | None = None,
    indoor: bool | None = None,
    has_lights: bool | None = None,
    min_price: int | None = None,
    max_price: int | None = None,
    min_rating: float | None = None,
    has_parking: bool | None = None,
    has_showers: bool | None = None,
    search: str | None = None,  # ADDED: Full-text search
) -> QuerySet[Court]:
    """
    Get courts with filtering and N+1 elimination.

    Optimizations:
    - Only active courts
    - Select related for foreign keys (future-proofing)
    - Database indexes on all filter fields

    Args:
        city: Filter by city (case-insensitive)
        surface_type: Surface type enum
        indoor: Boolean filter
        has_lights: Boolean filter
        min_price: Minimum price per hour
        max_price: Maximum price per hour
        min_rating: Minimum average rating
        has_parking: Boolean filter
        has_showers: Boolean filter
        search: Full-text search on name/address

    Returns:
        QuerySet of Court instances (lazy evaluation)
    """
    # Base queryset with select_related for future extensions
    queryset = Court.objects.filter(is_active=True)

    # Text search using PostgreSQL trigram (requires pg_trgm extension)
    if search:
        queryset = queryset.filter(
            models.Q(name__icontains=search) |
            models.Q(address__icontains=search) |
            models.Q(city__icontains=search)
        )

    if city:
        queryset = queryset.filter(city__iexact=city)

    if surface_type:
        queryset = queryset.filter(surface_type=surface_type)

    if indoor is not None:
        queryset = queryset.filter(indoor=indoor)

    if has_lights is not None:
        queryset = queryset.filter(has_lights=has_lights)

    if min_price is not None:
        queryset = queryset.filter(price_per_hour__gte=min_price)

    if max_price is not None:
        queryset = queryset.filter(price_per_hour__lte=max_price)

    if min_rating is not None:
        queryset = queryset.filter(average_rating__gte=min_rating)

    if has_parking is not None:
        queryset = queryset.filter(has_parking=has_parking)

    if has_showers is not None:
        queryset = queryset.filter(has_showers=has_showers)

    return queryset


def court_reviews_list(*, court_id: str) -> QuerySet[CourtReview]:
    """
    Get reviews for a court with user data prefetch.

    N+1 FIX: select_related('user') prevents query per review.

    Args:
        court_id: UUID of the court

    Returns:
        QuerySet of CourtReview with prefetched user data
    """
    return CourtReview.objects.filter(
        court_id=court_id
    ).select_related(
        "user"  # CRITICAL: Prevents N+1 on user data
    ).order_by("-created_at")


def court_get_user_review(*, court_id: str, user) -> CourtReview | None:
    """
    Get a specific user's review for a court.

    Args:
        court_id: UUID of the court
        user: User instance

    Returns:
        CourtReview or None if not found
    """
    try:
        return CourtReview.objects.get(court_id=court_id, user=user)
    except CourtReview.DoesNotExist:
        return None


def court_cities_list() -> list[str]:
    """
    Get distinct cities with active courts.

    Cached for 1 hour (rarely changes).

    Returns:
        List of city names
    """
    cache_key = "court_cities"
    cities = cache.get(cache_key)

    if cities is None:
        cities = list(
            Court.objects.filter(is_active=True)
            .values_list("city", flat=True)
            .distinct()
            .order_by("city")
        )
        cache.set(cache_key, cities, 3600)  # 1 hour

    return cities
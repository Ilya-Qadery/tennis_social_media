from django.contrib import admin

from .models import Court, CourtAvailability, CourtReview


@admin.register(Court)
class CourtAdmin(admin.ModelAdmin):
    list_display = [
        "name", "city", "surface_type", "indoor", "has_lights",
        "price_per_hour", "average_rating", "total_ratings", "is_active"
    ]
    list_filter = [
        "city", "surface_type", "indoor", "has_lights",
        "has_parking", "has_showers", "is_active"
    ]
    search_fields = ["name", "address", "city"]
    ordering = ["-created_at"]
    readonly_fields = ["created_at", "updated_at", "average_rating", "total_ratings"]


@admin.register(CourtReview)
class CourtReviewAdmin(admin.ModelAdmin):
    list_display = ["court", "user", "rating", "created_at"]
    list_filter = ["rating"]
    search_fields = ["court__name", "user__phone", "comment"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(CourtAvailability)
class CourtAvailabilityAdmin(admin.ModelAdmin):
    list_display = ["court", "day_of_week", "start_time", "end_time", "is_available"]
    list_filter = ["day_of_week", "is_available"]
    ordering = ["court", "day_of_week", "start_time"]

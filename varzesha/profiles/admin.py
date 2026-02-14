from django.contrib import admin

from .models import CoachProfile, PlayerProfile


@admin.register(PlayerProfile)
class PlayerProfileAdmin(admin.ModelAdmin):
    list_display = [
        "user", "ntrp_rating", "play_style", "years_experience",
        "city", "matches_played", "matches_won", "win_rate", "created_at"
    ]
    list_filter = ["play_style", "handedness", "city"]
    search_fields = ["user__phone", "user__first_name", "user__last_name", "city"]
    ordering = ["-created_at"]
    readonly_fields = ["created_at", "updated_at", "win_rate"]


@admin.register(CoachProfile)
class CoachProfileAdmin(admin.ModelAdmin):
    list_display = [
        "user", "is_verified", "years_experience", "hourly_rate",
        "city", "total_students", "rating", "created_at"
    ]
    list_filter = ["is_verified", "city"]
    search_fields = ["user__phone", "user__first_name", "user__last_name", "certification"]
    ordering = ["-created_at"]
    readonly_fields = ["created_at", "updated_at"]
    actions = ["verify_coaches"]
    
    @admin.action(description="Verify selected coaches")
    def verify_coaches(self, request, queryset):
        queryset.update(is_verified=True)

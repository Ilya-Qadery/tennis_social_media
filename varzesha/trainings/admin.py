from django.contrib import admin

from .models import Drill, TrainingDrill, TrainingGoal, TrainingSession


@admin.register(Drill)
class DrillAdmin(admin.ModelAdmin):
    list_display = [
        "name", "category", "difficulty", "duration_minutes",
        "usage_count", "is_public", "created_by"
    ]
    list_filter = ["category", "difficulty", "is_public"]
    search_fields = ["name", "description", "instructions"]
    ordering = ["category", "name"]


@admin.register(TrainingSession)
class TrainingSessionAdmin(admin.ModelAdmin):
    list_display = [
        "player", "date", "duration_minutes", "intensity",
        "feeling_score", "location_name", "created_at"
    ]
    list_filter = ["intensity", "date"]
    search_fields = ["player__phone", "title", "notes"]
    ordering = ["-date"]
    date_hierarchy = "date"


@admin.register(TrainingDrill)
class TrainingDrillAdmin(admin.ModelAdmin):
    list_display = [
        "training", "drill", "sets", "reps_per_set",
        "duration_minutes", "success_rate"
    ]
    list_filter = ["drill__category"]
    search_fields = ["training__player__phone", "drill__name"]


@admin.register(TrainingGoal)
class TrainingGoalAdmin(admin.ModelAdmin):
    list_display = [
        "player", "title", "current_value", "target_value",
        "progress_percentage", "status", "start_date", "end_date"
    ]
    list_filter = ["status"]
    search_fields = ["player__phone", "title", "description"]
    readonly_fields = ["created_at", "updated_at"]

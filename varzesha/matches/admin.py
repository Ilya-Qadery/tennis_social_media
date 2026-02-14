from django.contrib import admin

from .models import Match, MatchComment, MatchInvitation


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = [
        "id", "organizer", "opponent", "scheduled_at", "status",
        "match_type", "court", "is_public", "created_at"
    ]
    list_filter = ["status", "match_type", "is_public"]
    search_fields = [
        "organizer__phone", "opponent__phone",
        "title", "court_name"
    ]
    ordering = ["-scheduled_at"]
    readonly_fields = ["created_at", "updated_at"]
    date_hierarchy = "scheduled_at"


@admin.register(MatchInvitation)
class MatchInvitationAdmin(admin.ModelAdmin):
    list_display = [
        "match", "invited_by", "invited_user", "status", "created_at"
    ]
    list_filter = ["status"]
    search_fields = ["invited_by__phone", "invited_user__phone"]
    readonly_fields = ["created_at", "updated_at", "responded_at"]


@admin.register(MatchComment)
class MatchCommentAdmin(admin.ModelAdmin):
    list_display = ["match", "user", "content_preview", "created_at"]
    search_fields = ["user__phone", "content"]
    readonly_fields = ["created_at", "updated_at"]
    
    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = "Content"

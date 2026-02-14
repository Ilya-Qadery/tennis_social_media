"""
URL configuration for matches app.
"""
from django.urls import path

from .apis.match import (
    MatchAvailableListApi,
    MatchCancelApi,
    MatchCreateApi,
    MatchDetailApi,
    MatchJoinApi,
    MatchLeaveApi,
    MatchListApi,
    MatchRecordScoreApi,
    MatchStatsApi,
)

urlpatterns = [
    path("", MatchListApi.as_view(), name="match-list"),
    path("create/", MatchCreateApi.as_view(), name="match-create"),
    path("available/", MatchAvailableListApi.as_view(), name="match-available"),
    path("stats/", MatchStatsApi.as_view(), name="match-stats"),
    path("<uuid:match_id>/", MatchDetailApi.as_view(), name="match-detail"),
    path("<uuid:match_id>/join/", MatchJoinApi.as_view(), name="match-join"),
    path("<uuid:match_id>/leave/", MatchLeaveApi.as_view(), name="match-leave"),
    path("<uuid:match_id>/cancel/", MatchCancelApi.as_view(), name="match-cancel"),
    path("<uuid:match_id>/score/", MatchRecordScoreApi.as_view(), name="match-score"),
]

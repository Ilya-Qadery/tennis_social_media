"""
URL configuration for profiles app.
"""
from django.urls import path

from .apis.coach import (
    CoachProfileDetailApi,
    CoachProfileListApi,
    CoachProfilePublicApi,
)
from .apis.player import PlayerProfileDetailApi, PlayerProfileListApi

urlpatterns = [
    # Player profiles
    path("player/me/", PlayerProfileDetailApi.as_view(), name="player-profile-me"),
    path("players/", PlayerProfileListApi.as_view(), name="player-profile-list"),
    
    # Coach profiles
    path("coach/me/", CoachProfileDetailApi.as_view(), name="coach-profile-me"),
    path("coaches/", CoachProfileListApi.as_view(), name="coach-profile-list"),
    path("coaches/<uuid:user_id>/", CoachProfilePublicApi.as_view(), name="coach-profile-public"),
]

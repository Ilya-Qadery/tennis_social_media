"""
URL configuration for courts app.
"""
from django.urls import path

from .apis.court import (
    CourtCitiesApi,
    CourtDetailApi,
    CourtListApi,
    CourtReviewListApi,
)

urlpatterns = [
    path("", CourtListApi.as_view(), name="court-list"),
    path("cities/", CourtCitiesApi.as_view(), name="court-cities"),
    path("<uuid:court_id>/", CourtDetailApi.as_view(), name="court-detail"),
    path("<uuid:court_id>/reviews/", CourtReviewListApi.as_view(), name="court-reviews"),
]

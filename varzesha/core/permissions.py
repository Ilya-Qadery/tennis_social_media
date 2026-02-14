"""
Object-level permissions following HackSoft style guide.
"""
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import View

from varzesha.courts.models import Court, CourtReview
from varzesha.matches.models import Match
from varzesha.profiles.models import CoachProfile, PlayerProfile
from varzesha.trainings.models import TrainingSession, TrainingGoal


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners to edit.
    """

    def has_object_permission(self, request: Request, view: View, obj) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True

        # Handle different model types
        if hasattr(obj, "user"):
            return obj.user == request.user
        if hasattr(obj, "player"):
            return obj.player == request.user
        if hasattr(obj, "organizer"):
            return obj.organizer == request.user

        return False


class IsMatchParticipant(permissions.BasePermission):
    """
    Permission for match participants only.
    """

    def has_object_permission(self, request: Request, view: View, obj: Match) -> bool:
        return request.user in [obj.organizer, obj.opponent]


class IsVerifiedCoach(permissions.BasePermission):
    """
    Permission for verified coaches only.
    """

    def has_permission(self, request: Request, view: View) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False

        try:
            return request.user.coach_profile.is_verified
        except CoachProfile.DoesNotExist:
            return False


class IsPhoneVerified(permissions.BasePermission):
    """
    Permission for phone-verified users only.
    """

    def has_permission(self, request: Request, view: View) -> bool:
        return (
                request.user
                and request.user.is_authenticated
                and request.user.is_phone_verified
        )
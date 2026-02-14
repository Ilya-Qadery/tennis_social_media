"""
Player profile APIs.
"""
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from varzesha.core.exceptions import ApplicationError, ValidationError

from ..models import PlayStyle, Handedness
from ..selectors import (
    player_profile_get_by_user,
    player_profile_list,
)
from ..services import player_profile_create, player_profile_update


class PlayerProfileDetailApi(APIView):
    """API to get/update current user's player profile."""
    
    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        user_id = serializers.UUIDField(source="user.id")
        phone = serializers.CharField(source="user.phone")
        full_name = serializers.CharField(source="user.full_name")
        ntrp_rating = serializers.DecimalField(max_digits=2, decimal_places=1)
        play_style = serializers.CharField()
        play_style_display = serializers.CharField(source="get_play_style_display")
        handedness = serializers.CharField()
        handedness_display = serializers.CharField(source="get_handedness_display")
        years_experience = serializers.IntegerField()
        height_cm = serializers.IntegerField()
        weight_kg = serializers.IntegerField()
        bio = serializers.CharField()
        avatar = serializers.ImageField()
        city = serializers.CharField()
        matches_played = serializers.IntegerField()
        matches_won = serializers.IntegerField()
        win_rate = serializers.FloatField()
        created_at = serializers.DateTimeField()
    
    class UpdateSerializer(serializers.Serializer):
        ntrp_rating = serializers.DecimalField(
            max_digits=2, decimal_places=1, required=False
        )
        play_style = serializers.ChoiceField(
            choices=PlayStyle.choices, required=False
        )
        handedness = serializers.ChoiceField(
            choices=Handedness.choices, required=False
        )
        years_experience = serializers.IntegerField(required=False, min_value=0)
        height_cm = serializers.IntegerField(required=False, min_value=50)
        weight_kg = serializers.IntegerField(required=False, min_value=20)
        bio = serializers.CharField(required=False, allow_blank=True)
        city = serializers.CharField(required=False, allow_blank=True)
    
    def get(self, request):
        """Get current user's player profile."""
        profile = player_profile_get_by_user(user=request.user)
        if not profile:
            return Response(
                {"message": "Player profile not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(self.OutputSerializer(profile).data)
    
    def post(self, request):
        """Create player profile for current user."""
        if player_profile_get_by_user(user=request.user):
            return Response(
                {"message": "Player profile already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            profile = player_profile_create(user=request.user)
        except ValidationError as e:
            return Response(
                {"message": e.message},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(
            self.OutputSerializer(profile).data,
            status=status.HTTP_201_CREATED
        )
    
    def patch(self, request):
        """Update current user's player profile."""
        profile = player_profile_get_by_user(user=request.user)
        if not profile:
            return Response(
                {"message": "Player profile not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = self.UpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            profile = player_profile_update(
                profile=profile,
                data=serializer.validated_data
            )
        except ValidationError as e:
            return Response(
                {"message": e.message},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(self.OutputSerializer(profile).data)


class PlayerProfileListApi(APIView):
    """API to list player profiles with filtering."""
    
    permission_classes = []
    authentication_classes = []
    
    class FilterSerializer(serializers.Serializer):
        city = serializers.CharField(required=False)
        ntrp_min = serializers.DecimalField(
            max_digits=2, decimal_places=1, required=False
        )
        ntrp_max = serializers.DecimalField(
            max_digits=2, decimal_places=1, required=False
        )
        play_style = serializers.ChoiceField(
            choices=PlayStyle.choices, required=False
        )
    
    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        user_id = serializers.UUIDField(source="user.id")
        full_name = serializers.CharField(source="user.full_name")
        ntrp_rating = serializers.DecimalField(max_digits=2, decimal_places=1)
        play_style_display = serializers.CharField(source="get_play_style_display")
        city = serializers.CharField()
        matches_played = serializers.IntegerField()
        win_rate = serializers.FloatField()
        avatar = serializers.ImageField()
    
    def get(self, request):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)
        
        profiles = player_profile_list(**filters_serializer.validated_data)
        
        # Pagination could be added here
        return Response(self.OutputSerializer(profiles, many=True).data)

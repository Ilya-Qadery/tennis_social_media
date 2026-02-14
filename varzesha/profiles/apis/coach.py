"""
Coach profile APIs.
"""
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from varzesha.core.exceptions import ValidationError

from ..selectors import (
    coach_profile_get,
    coach_profile_get_by_user,
    coach_profile_list,
)
from ..services import coach_profile_create, coach_profile_update


class CoachProfileDetailApi(APIView):
    """API to get/update current user's coach profile."""
    
    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        user_id = serializers.UUIDField(source="user.id")
        phone = serializers.CharField(source="user.phone")
        full_name = serializers.CharField(source="user.full_name")
        is_verified = serializers.BooleanField()
        certification = serializers.CharField()
        years_experience = serializers.IntegerField()
        hourly_rate = serializers.IntegerField()
        specialties = serializers.ListField()
        bio = serializers.CharField()
        avatar = serializers.ImageField()
        city = serializers.CharField()
        available_days = serializers.ListField()
        total_students = serializers.IntegerField()
        rating = serializers.DecimalField(max_digits=2, decimal_places=1)
        created_at = serializers.DateTimeField()
    
    class UpdateSerializer(serializers.Serializer):
        certification = serializers.CharField(required=False, allow_blank=True)
        years_experience = serializers.IntegerField(required=False, min_value=0)
        hourly_rate = serializers.IntegerField(required=False, min_value=0)
        specialties = serializers.ListField(required=False)
        bio = serializers.CharField(required=False, allow_blank=True)
        city = serializers.CharField(required=False, allow_blank=True)
        available_days = serializers.ListField(required=False)
    
    class CreateSerializer(serializers.Serializer):
        certification = serializers.CharField(required=False, allow_blank=True)
        years_experience = serializers.IntegerField(required=False, default=0)
        hourly_rate = serializers.IntegerField(required=False)
        bio = serializers.CharField(required=False, allow_blank=True)
    
    def get(self, request):
        """Get current user's coach profile."""
        profile = coach_profile_get_by_user(user=request.user)
        if not profile:
            return Response(
                {"message": "Coach profile not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(self.OutputSerializer(profile).data)
    
    def post(self, request):
        """Create coach profile for current user."""
        if coach_profile_get_by_user(user=request.user):
            return Response(
                {"message": "Coach profile already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.CreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            profile = coach_profile_create(
                user=request.user,
                **serializer.validated_data
            )
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
        """Update current user's coach profile."""
        profile = coach_profile_get_by_user(user=request.user)
        if not profile:
            return Response(
                {"message": "Coach profile not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = self.UpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            profile = coach_profile_update(
                profile=profile,
                data=serializer.validated_data
            )
        except ValidationError as e:
            return Response(
                {"message": e.message},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(self.OutputSerializer(profile).data)


class CoachProfileListApi(APIView):
    """API to list coach profiles with filtering."""
    
    permission_classes = []
    authentication_classes = []
    
    class FilterSerializer(serializers.Serializer):
        city = serializers.CharField(required=False)
        is_verified = serializers.BooleanField(required=False)
        min_rate = serializers.IntegerField(required=False, min_value=0)
        max_rate = serializers.IntegerField(required=False, min_value=0)
    
    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        user_id = serializers.UUIDField(source="user.id")
        full_name = serializers.CharField(source="user.full_name")
        is_verified = serializers.BooleanField()
        years_experience = serializers.IntegerField()
        hourly_rate = serializers.IntegerField()
        city = serializers.CharField()
        rating = serializers.DecimalField(max_digits=2, decimal_places=1)
        avatar = serializers.ImageField()
    
    def get(self, request):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)
        
        profiles = coach_profile_list(**filters_serializer.validated_data)
        
        return Response(self.OutputSerializer(profiles, many=True).data)


class CoachProfilePublicApi(APIView):
    """API to get public coach profile details."""
    
    permission_classes = []
    authentication_classes = []
    
    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        user_id = serializers.UUIDField(source="user.id")
        full_name = serializers.CharField(source="user.full_name")
        is_verified = serializers.BooleanField()
        certification = serializers.CharField()
        years_experience = serializers.IntegerField()
        hourly_rate = serializers.IntegerField()
        specialties = serializers.ListField()
        bio = serializers.CharField()
        avatar = serializers.ImageField()
        city = serializers.CharField()
        available_days = serializers.ListField()
        total_students = serializers.IntegerField()
        rating = serializers.DecimalField(max_digits=2, decimal_places=1)
    
    def get(self, request, user_id):
        try:
            profile = coach_profile_get(user_id=user_id)
        except Exception:
            return Response(
                {"message": "Coach profile not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response(self.OutputSerializer(profile).data)

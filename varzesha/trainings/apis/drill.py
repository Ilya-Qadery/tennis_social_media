"""
Drill APIs.
"""
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from varzesha.core.exceptions import ValidationError

from ..models import DifficultyLevel, DrillCategory
from ..selectors import drill_get, drill_list
from ..services import drill_create, drill_update


class DrillListApi(APIView):
    """API to list drills with filtering."""
    
    permission_classes = []
    authentication_classes = []
    
    class FilterSerializer(serializers.Serializer):
        category = serializers.ChoiceField(
            choices=DrillCategory.choices, required=False
        )
        difficulty = serializers.ChoiceField(
            choices=DifficultyLevel.choices, required=False
        )
    
    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        name = serializers.CharField()
        category = serializers.CharField()
        category_display = serializers.CharField(source="get_category_display")
        difficulty = serializers.CharField()
        difficulty_display = serializers.CharField(source="get_difficulty_display")
        duration_minutes = serializers.IntegerField()
        description = serializers.CharField()
        equipment_needed = serializers.ListField()
        image = serializers.ImageField()
        usage_count = serializers.IntegerField()
    
    def get(self, request):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)
        
        drills = drill_list(**filters_serializer.validated_data)
        return Response(self.OutputSerializer(drills, many=True).data)


class DrillDetailApi(APIView):
    """API to get drill details."""
    
    permission_classes = []
    authentication_classes = []
    
    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        name = serializers.CharField()
        category = serializers.CharField()
        category_display = serializers.CharField(source="get_category_display")
        difficulty = serializers.CharField()
        difficulty_display = serializers.CharField(source="get_difficulty_display")
        duration_minutes = serializers.IntegerField()
        description = serializers.CharField()
        instructions = serializers.CharField()
        tips = serializers.CharField()
        equipment_needed = serializers.ListField()
        video_url = serializers.CharField()
        image = serializers.ImageField()
        usage_count = serializers.IntegerField()
        created_by = serializers.SerializerMethodField()
    
    def get_created_by(self, obj):
        if obj.created_by:
            return {
                "id": obj.created_by.id,
                "name": obj.created_by.full_name,
            }
        return None
    
    def get(self, request, drill_id):
        try:
            drill = drill_get(drill_id=drill_id)
        except Exception:
            return Response(
                {"message": "Drill not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response(self.OutputSerializer(drill).data)


class DrillCreateApi(APIView):
    """API to create a new drill (for coaches/admins)."""
    
    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=255)
        category = serializers.ChoiceField(choices=DrillCategory.choices)
        description = serializers.CharField()
        instructions = serializers.CharField()
        difficulty = serializers.ChoiceField(
            choices=DifficultyLevel.choices, required=False
        )
        duration_minutes = serializers.IntegerField(required=False, default=15)
        equipment_needed = serializers.ListField(required=False, default=list)
        tips = serializers.CharField(required=False, allow_blank=True)
        video_url = serializers.URLField(required=False, allow_blank=True)
        is_public = serializers.BooleanField(required=False, default=True)
    
    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        name = serializers.CharField()
        category = serializers.CharField()
        difficulty = serializers.CharField()
    
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            drill = drill_create(
                created_by=request.user,
                **serializer.validated_data
            )
        except ValidationError as e:
            return Response(
                {"message": e.message},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(
            self.OutputSerializer(drill).data,
            status=status.HTTP_201_CREATED
        )

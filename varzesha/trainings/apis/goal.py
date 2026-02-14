"""
Training goal APIs.
"""
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from varzesha.core.exceptions import PermissionDeniedError, ValidationError

from ..selectors import training_goal_get, training_goal_list
from ..services import (
    training_goal_create,
    training_goal_update,
    training_goal_update_progress,
)


class TrainingGoalListApi(APIView):
    """API to list user's training goals."""
    
    class FilterSerializer(serializers.Serializer):
        status = serializers.CharField(required=False)
    
    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        title = serializers.CharField()
        description = serializers.CharField()
        target_value = serializers.IntegerField()
        current_value = serializers.IntegerField()
        progress_percentage = serializers.IntegerField()
        start_date = serializers.DateField()
        end_date = serializers.DateField()
        status = serializers.CharField()
        status_display = serializers.CharField(source="get_status_display")
        created_at = serializers.DateTimeField()
    
    def get(self, request):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)
        
        goals = training_goal_list(
            user=request.user,
            **filters_serializer.validated_data
        )
        return Response(self.OutputSerializer(goals, many=True).data)


class TrainingGoalCreateApi(APIView):
    """API to create a training goal."""
    
    class InputSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=255)
        description = serializers.CharField(required=False, allow_blank=True)
        target_value = serializers.IntegerField(min_value=1)
        start_date = serializers.DateField()
        end_date = serializers.DateField(required=False, allow_null=True)
    
    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        title = serializers.CharField()
        target_value = serializers.IntegerField()
        progress_percentage = serializers.IntegerField()
        status = serializers.CharField()
    
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            goal = training_goal_create(
                player=request.user,
                **serializer.validated_data
            )
        except ValidationError as e:
            return Response(
                {"message": e.message},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(
            self.OutputSerializer(goal).data,
            status=status.HTTP_201_CREATED
        )


class TrainingGoalDetailApi(APIView):
    """API to get/update a training goal."""
    
    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        title = serializers.CharField()
        description = serializers.CharField()
        target_value = serializers.IntegerField()
        current_value = serializers.IntegerField()
        progress_percentage = serializers.IntegerField()
        start_date = serializers.DateField()
        end_date = serializers.DateField()
        status = serializers.CharField()
        status_display = serializers.CharField(source="get_status_display")
        created_at = serializers.DateTimeField()
    
    class UpdateSerializer(serializers.Serializer):
        title = serializers.CharField(required=False)
        description = serializers.CharField(required=False, allow_blank=True)
        target_value = serializers.IntegerField(required=False, min_value=1)
        end_date = serializers.DateField(required=False, allow_null=True)
        status = serializers.CharField(required=False)
    
    def get(self, request, goal_id):
        try:
            goal = training_goal_get(goal_id=goal_id, user=request.user)
        except Exception:
            return Response(
                {"message": "Goal not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response(self.OutputSerializer(goal).data)
    
    def patch(self, request, goal_id):
        try:
            goal = training_goal_get(goal_id=goal_id, user=request.user)
        except Exception:
            return Response(
                {"message": "Goal not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = self.UpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            goal = training_goal_update(
                goal=goal,
                user=request.user,
                data=serializer.validated_data
            )
        except (ValidationError, PermissionDeniedError) as e:
            return Response(
                {"message": e.message},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(self.OutputSerializer(goal).data)


class TrainingGoalProgressApi(APIView):
    """API to update goal progress."""
    
    class InputSerializer(serializers.Serializer):
        increment = serializers.IntegerField(default=1, min_value=1)
    
    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        current_value = serializers.IntegerField()
        target_value = serializers.IntegerField()
        progress_percentage = serializers.IntegerField()
        status = serializers.CharField()
    
    def post(self, request, goal_id):
        try:
            goal = training_goal_get(goal_id=goal_id, user=request.user)
        except Exception:
            return Response(
                {"message": "Goal not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        goal = training_goal_update_progress(
            goal=goal,
            increment=serializer.validated_data.get("increment", 1)
        )
        
        return Response(self.OutputSerializer(goal).data)

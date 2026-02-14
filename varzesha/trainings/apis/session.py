"""
Training session APIs.
"""
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from varzesha.core.exceptions import PermissionDeniedError, ValidationError

from ..models import IntensityLevel
from ..selectors import (
    training_drill_list,
    training_session_get,
    training_session_list,
    training_session_get_stats,
)
from ..services import (
    training_drill_add,
    training_drill_remove,
    training_drill_update,
    training_session_create,
    training_session_delete,
    training_session_update,
)


class TrainingSessionListApi(APIView):
    """API to list user's training sessions."""
    
    class FilterSerializer(serializers.Serializer):
        date_from = serializers.DateField(required=False)
        date_to = serializers.DateField(required=False)
    
    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        title = serializers.CharField()
        date = serializers.DateField()
        duration_minutes = serializers.IntegerField()
        intensity = serializers.CharField()
        intensity_display = serializers.CharField(source="get_intensity_display")
        location_name = serializers.CharField()
        feeling_score = serializers.IntegerField()
        notes = serializers.CharField()
        drill_count = serializers.SerializerMethodField()
    
    def get_drill_count(self, obj):
        return obj.drills.count()
    
    def get(self, request):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)
        
        sessions = training_session_list(
            user=request.user,
            **filters_serializer.validated_data
        )
        return Response(self.OutputSerializer(sessions, many=True).data)


class TrainingSessionCreateApi(APIView):
    """API to create a training session."""
    
    class InputSerializer(serializers.Serializer):
        title = serializers.CharField(required=False, allow_blank=True)
        date = serializers.DateField()
        duration_minutes = serializers.IntegerField(min_value=1)
        intensity = serializers.ChoiceField(
            choices=IntensityLevel.choices, default="medium"
        )
        court_id = serializers.UUIDField(required=False, allow_null=True)
        location_name = serializers.CharField(required=False, allow_blank=True)
        notes = serializers.CharField(required=False, allow_blank=True)
        feeling_score = serializers.IntegerField(
            required=False, min_value=1, max_value=5, allow_null=True
        )
    
    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        title = serializers.CharField()
        date = serializers.DateField()
        duration_minutes = serializers.IntegerField()
        intensity = serializers.CharField()
    
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        
        # Get court if provided
        court = None
        if data.get("court_id"):
            from varzesha.courts.selectors import court_get
            try:
                court = court_get(court_id=data.pop("court_id"))
            except Exception:
                return Response(
                    {"message": "Court not found."},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        try:
            session = training_session_create(
                player=request.user,
                court=court,
                **data
            )
        except ValidationError as e:
            return Response(
                {"message": e.message},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(
            self.OutputSerializer(session).data,
            status=status.HTTP_201_CREATED
        )


class TrainingSessionDetailApi(APIView):
    """API to get/update/delete a training session."""
    
    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        title = serializers.CharField()
        date = serializers.DateField()
        duration_minutes = serializers.IntegerField()
        intensity = serializers.CharField()
        intensity_display = serializers.CharField(source="get_intensity_display")
        location_name = serializers.CharField()
        notes = serializers.CharField()
        feeling_score = serializers.IntegerField()
        court = serializers.SerializerMethodField()
        drills = serializers.SerializerMethodField()
        created_at = serializers.DateTimeField()
    
    def get_court(self, obj):
        if obj.court:
            return {
                "id": obj.court.id,
                "name": obj.court.name,
            }
        return None
    
    def get_drills(self, obj):
        drills = training_drill_list(session_id=obj.id)
        return [{
            "id": d.id,
            "drill_id": d.drill.id,
            "drill_name": d.drill.name,
            "sets": d.sets,
            "reps_per_set": d.reps_per_set,
            "duration_minutes": d.duration_minutes,
            "success_rate": d.success_rate,
        } for d in drills]
    
    class UpdateSerializer(serializers.Serializer):
        title = serializers.CharField(required=False, allow_blank=True)
        date = serializers.DateField(required=False)
        duration_minutes = serializers.IntegerField(required=False, min_value=1)
        intensity = serializers.ChoiceField(
            choices=IntensityLevel.choices, required=False
        )
        location_name = serializers.CharField(required=False, allow_blank=True)
        notes = serializers.CharField(required=False, allow_blank=True)
        feeling_score = serializers.IntegerField(
            required=False, min_value=1, max_value=5, allow_null=True
        )
    
    def get(self, request, session_id):
        try:
            session = training_session_get(session_id=session_id, user=request.user)
        except Exception:
            return Response(
                {"message": "Training session not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response(self.OutputSerializer(session).data)
    
    def patch(self, request, session_id):
        try:
            session = training_session_get(session_id=session_id, user=request.user)
        except Exception:
            return Response(
                {"message": "Training session not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = self.UpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            session = training_session_update(
                session=session,
                user=request.user,
                data=serializer.validated_data
            )
        except (ValidationError, PermissionDeniedError) as e:
            return Response(
                {"message": e.message},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(self.OutputSerializer(session).data)
    
    def delete(self, request, session_id):
        try:
            session = training_session_get(session_id=session_id, user=request.user)
        except Exception:
            return Response(
                {"message": "Training session not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        try:
            training_session_delete(session=session, user=request.user)
        except PermissionDeniedError as e:
            return Response(
                {"message": e.message},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return Response(status=status.HTTP_204_NO_CONTENT)


class TrainingSessionAddDrillApi(APIView):
    """API to add a drill to a training session."""
    
    class InputSerializer(serializers.Serializer):
        drill_id = serializers.UUIDField()
        sets = serializers.IntegerField(default=1, min_value=1)
        reps_per_set = serializers.IntegerField(default=10, min_value=1)
        duration_minutes = serializers.IntegerField(required=False, allow_null=True)
        notes = serializers.CharField(required=False, allow_blank=True)
    
    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        drill_name = serializers.CharField(source="drill.name")
        sets = serializers.IntegerField()
        reps_per_set = serializers.IntegerField()
    
    def post(self, request, session_id):
        try:
            session = training_session_get(session_id=session_id, user=request.user)
        except Exception:
            return Response(
                {"message": "Training session not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        
        # Get drill
        from varzesha.trainings.selectors import drill_get
        try:
            drill = drill_get(drill_id=data.pop("drill_id"))
        except Exception:
            return Response(
                {"message": "Drill not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        try:
            training_drill = training_drill_add(
                training=session,
                drill=drill,
                **data
            )
        except ValidationError as e:
            return Response(
                {"message": e.message},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(
            self.OutputSerializer(training_drill).data,
            status=status.HTTP_201_CREATED
        )


class TrainingSessionRemoveDrillApi(APIView):
    """API to remove a drill from a training session."""
    
    def delete(self, request, session_id, drill_instance_id):
        try:
            session = training_session_get(session_id=session_id, user=request.user)
        except Exception:
            return Response(
                {"message": "Training session not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        try:
            training_drill = session.drills.get(id=drill_instance_id)
        except Exception:
            return Response(
                {"message": "Drill not found in this session."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        try:
            training_drill_remove(training_drill=training_drill, user=request.user)
        except PermissionDeniedError as e:
            return Response(
                {"message": e.message},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return Response(status=status.HTTP_204_NO_CONTENT)


class TrainingStatsApi(APIView):
    """API to get user's training statistics."""
    
    def get(self, request):
        stats = training_session_get_stats(user=request.user)
        return Response(stats)

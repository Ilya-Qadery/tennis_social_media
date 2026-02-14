"""
Match APIs.
"""
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from varzesha.core.exceptions import PermissionDeniedError, ValidationError

from ..models import MatchStatus, MatchType
from ..selectors import (
    match_get,
    match_list,
    match_list_available,
    match_get_user_stats,
)
from ..services import (
    match_cancel,
    match_create,
    match_join,
    match_leave,
    match_record_score,
    match_update,
)


class MatchListApi(APIView):
    """API to list user's matches."""
    
    class FilterSerializer(serializers.Serializer):
        status = serializers.ChoiceField(
            choices=MatchStatus.choices, required=False
        )
        upcoming = serializers.BooleanField(required=False)
        past = serializers.BooleanField(required=False)
    
    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        title = serializers.CharField()
        description = serializers.CharField()
        match_type = serializers.CharField()
        status = serializers.CharField()
        status_display = serializers.CharField(source="get_status_display")
        scheduled_at = serializers.DateTimeField()
        duration_minutes = serializers.IntegerField()
        court_name = serializers.CharField()
        court = serializers.SerializerMethodField()
        organizer = serializers.SerializerMethodField()
        opponent = serializers.SerializerMethodField()
        can_join = serializers.BooleanField()
        is_organizer = serializers.SerializerMethodField()
    
    def get_court(self, obj):
        if obj.court:
            return {
                "id": obj.court.id,
                "name": obj.court.name,
                "city": obj.court.city,
            }
        return None
    
    def get_organizer(self, obj):
        return {
            "id": obj.organizer.id,
            "name": obj.organizer.full_name,
            "phone": obj.organizer.phone,
        }
    
    def get_opponent(self, obj):
        if obj.opponent:
            return {
                "id": obj.opponent.id,
                "name": obj.opponent.full_name,
                "phone": obj.opponent.phone,
            }
        return None
    
    def get_is_organizer(self, obj):
        request = self.context.get("request")
        if request:
            return obj.organizer == request.user
        return False
    
    def get(self, request):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)
        
        matches = match_list(
            user=request.user,
            **filters_serializer.validated_data
        )
        
        serializer = self.OutputSerializer(
            matches, many=True, context={"request": request}
        )
        return Response(serializer.data)


class MatchAvailableListApi(APIView):
    """API to list available public matches."""
    
    permission_classes = []
    authentication_classes = []
    
    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        title = serializers.CharField()
        description = serializers.CharField()
        scheduled_at = serializers.DateTimeField()
        duration_minutes = serializers.IntegerField()
        court_name = serializers.CharField()
        court = serializers.SerializerMethodField()
        organizer = serializers.SerializerMethodField()
        ntrp_min = serializers.DecimalField(max_digits=2, decimal_places=1)
        ntrp_max = serializers.DecimalField(max_digits=2, decimal_places=1)
    
    def get_court(self, obj):
        if obj.court:
            return {
                "id": obj.court.id,
                "name": obj.court.name,
                "city": obj.court.city,
            }
        return None
    
    def get_organizer(self, obj):
        return {
            "id": obj.organizer.id,
            "name": obj.organizer.full_name,
        }
    
    def get(self, request):
        matches = match_list_available(user=request.user if request.user.is_authenticated else None)
        return Response(self.OutputSerializer(matches, many=True).data)


class MatchCreateApi(APIView):
    """API to create a new match."""
    
    class InputSerializer(serializers.Serializer):
        title = serializers.CharField(required=False, allow_blank=True)
        description = serializers.CharField(required=False, allow_blank=True)
        scheduled_at = serializers.DateTimeField()
        duration_minutes = serializers.IntegerField(default=90, min_value=30)
        court_id = serializers.UUIDField(required=False, allow_null=True)
        court_name = serializers.CharField(required=False, allow_blank=True)
        match_type = serializers.ChoiceField(
            choices=MatchType.choices, default="singles"
        )
        ntrp_min = serializers.DecimalField(
            max_digits=2, decimal_places=1, required=False, allow_null=True
        )
        ntrp_max = serializers.DecimalField(
            max_digits=2, decimal_places=1, required=False, allow_null=True
        )
        is_public = serializers.BooleanField(default=True)
    
    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        title = serializers.CharField()
        scheduled_at = serializers.DateTimeField()
        status = serializers.CharField()
    
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        
        # Get court if provided
        court = None
        if data.get("court_id"):
            from varzesha.courts.selectors import court_get
            try:
                court = court_get(court_id=data["court_id"])
            except Exception:
                return Response(
                    {"message": "Court not found."},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        try:
            match = match_create(
                organizer=request.user,
                title=data.get("title", ""),
                description=data.get("description", ""),
                scheduled_at=data["scheduled_at"],
                duration_minutes=data.get("duration_minutes", 90),
                court=court,
                court_name=data.get("court_name", ""),
                match_type=data.get("match_type", "singles"),
                ntrp_min=data.get("ntrp_min"),
                ntrp_max=data.get("ntrp_max"),
                is_public=data.get("is_public", True),
            )
        except ValidationError as e:
            return Response(
                {"message": e.message},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(
            self.OutputSerializer(match).data,
            status=status.HTTP_201_CREATED
        )


class MatchDetailApi(APIView):
    """API to get/update/cancel a match."""
    
    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        title = serializers.CharField()
        description = serializers.CharField()
        match_type = serializers.CharField()
        match_type_display = serializers.CharField(source="get_match_type_display")
        status = serializers.CharField()
        status_display = serializers.CharField(source="get_status_display")
        scheduled_at = serializers.DateTimeField()
        duration_minutes = serializers.IntegerField()
        court = serializers.SerializerMethodField()
        court_name = serializers.CharField()
        organizer = serializers.SerializerMethodField()
        opponent = serializers.SerializerMethodField()
        ntrp_min = serializers.DecimalField(max_digits=2, decimal_places=1)
        ntrp_max = serializers.DecimalField(max_digits=2, decimal_places=1)
        organizer_score = serializers.IntegerField()
        opponent_score = serializers.IntegerField()
        set_scores = serializers.ListField()
        winner = serializers.SerializerMethodField()
        is_public = serializers.BooleanField()
        created_at = serializers.DateTimeField()
    
    def get_court(self, obj):
        if obj.court:
            return {
                "id": obj.court.id,
                "name": obj.court.name,
                "address": obj.court.address,
            }
        return None
    
    def get_organizer(self, obj):
        return {
            "id": obj.organizer.id,
            "name": obj.organizer.full_name,
            "phone": obj.organizer.phone,
        }
    
    def get_opponent(self, obj):
        if obj.opponent:
            return {
                "id": obj.opponent.id,
                "name": obj.opponent.full_name,
                "phone": obj.opponent.phone,
            }
        return None
    
    def get_winner(self, obj):
        if obj.winner:
            return {
                "id": obj.winner.id,
                "name": obj.winner.full_name,
            }
        return None
    
    def get(self, request, match_id):
        try:
            match = match_get(match_id=match_id)
        except Exception:
            return Response(
                {"message": "Match not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response(self.OutputSerializer(match).data)
    
    def patch(self, request, match_id):
        try:
            match = match_get(match_id=match_id)
        except Exception:
            return Response(
                {"message": "Match not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Only allow updating certain fields
        allowed_fields = [
            "title", "description", "scheduled_at", "court_id",
            "court_name", "ntrp_min", "ntrp_max", "is_public", "duration_minutes"
        ]
        update_data = {k: v for k, v in request.data.items() if k in allowed_fields}
        
        # Handle court_id separately
        if "court_id" in update_data:
            from varzesha.courts.selectors import court_get
            try:
                court = court_get(court_id=update_data.pop("court_id"))
                update_data["court"] = court
            except Exception:
                return Response(
                    {"message": "Court not found."},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        try:
            match = match_update(match=match, user=request.user, data=update_data)
        except (ValidationError, PermissionDeniedError) as e:
            return Response(
                {"message": e.message},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(self.OutputSerializer(match).data)


class MatchJoinApi(APIView):
    """API to join a public match."""
    
    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        status = serializers.CharField()
        opponent = serializers.SerializerMethodField()
    
    def get_opponent(self, obj):
        if obj.opponent:
            return {
                "id": obj.opponent.id,
                "name": obj.opponent.full_name,
            }
        return None
    
    def post(self, request, match_id):
        try:
            match = match_get(match_id=match_id)
        except Exception:
            return Response(
                {"message": "Match not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        try:
            match = match_join(match=match, user=request.user)
        except ValidationError as e:
            return Response(
                {"message": e.message},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(self.OutputSerializer(match).data)


class MatchLeaveApi(APIView):
    """API to leave a match as opponent."""
    
    def post(self, request, match_id):
        try:
            match = match_get(match_id=match_id)
        except Exception:
            return Response(
                {"message": "Match not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        try:
            match = match_leave(match=match, user=request.user)
        except (ValidationError, PermissionDeniedError) as e:
            return Response(
                {"message": e.message},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response({"status": match.status, "opponent": None})


class MatchCancelApi(APIView):
    """API to cancel a match."""
    
    class InputSerializer(serializers.Serializer):
        reason = serializers.CharField(required=False, allow_blank=True)
    
    def post(self, request, match_id):
        try:
            match = match_get(match_id=match_id)
        except Exception:
            return Response(
                {"message": "Match not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            match = match_cancel(
                match=match,
                user=request.user,
                reason=serializer.validated_data.get("reason", "")
            )
        except (ValidationError, PermissionDeniedError) as e:
            return Response(
                {"message": e.message},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response({"status": match.status, "cancelled_by": request.user.id})


class MatchRecordScoreApi(APIView):
    """API to record match score."""
    
    class InputSerializer(serializers.Serializer):
        organizer_score = serializers.IntegerField(min_value=0)
        opponent_score = serializers.IntegerField(min_value=0)
        set_scores = serializers.ListField(required=False)
    
    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        status = serializers.CharField()
        organizer_score = serializers.IntegerField()
        opponent_score = serializers.IntegerField()
        winner = serializers.SerializerMethodField()
    
    def get_winner(self, obj):
        if obj.winner:
            return {
                "id": obj.winner.id,
                "name": obj.winner.full_name,
            }
        return None
    
    def post(self, request, match_id):
        try:
            match = match_get(match_id=match_id)
        except Exception:
            return Response(
                {"message": "Match not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            match = match_record_score(
                match=match,
                user=request.user,
                **serializer.validated_data
            )
        except (ValidationError, PermissionDeniedError) as e:
            return Response(
                {"message": e.message},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(self.OutputSerializer(match).data)


class MatchStatsApi(APIView):
    """API to get user's match statistics."""
    
    def get(self, request):
        stats = match_get_user_stats(user=request.user)
        return Response(stats)

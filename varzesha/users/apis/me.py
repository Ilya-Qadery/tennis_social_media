"""
Current user APIs (me endpoints).
"""
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from varzesha.core.exceptions import ApplicationError, ValidationError

from ..services import user_change_password, user_update


class UserMeApi(APIView):
    """API to get/update current user info."""
    
    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        phone = serializers.CharField()
        email = serializers.EmailField()
        first_name = serializers.CharField()
        last_name = serializers.CharField()
        full_name = serializers.CharField()
        is_phone_verified = serializers.BooleanField()
        is_coach = serializers.BooleanField()
        created_at = serializers.DateTimeField()
    
    class UpdateSerializer(serializers.Serializer):
        first_name = serializers.CharField(required=False, allow_blank=True)
        last_name = serializers.CharField(required=False, allow_blank=True)
        email = serializers.EmailField(required=False, allow_blank=True)
    
    def get(self, request):
        """Get current user info."""
        return Response(self.OutputSerializer(request.user).data)
    
    def patch(self, request):
        """Update current user info."""
        serializer = self.UpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            user = user_update(user=request.user, data=serializer.validated_data)
        except ValidationError as e:
            return Response(
                {"message": e.message},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(self.OutputSerializer(user).data)


class UserChangePasswordApi(APIView):
    """API to change user password."""
    
    class InputSerializer(serializers.Serializer):
        old_password = serializers.CharField(write_only=True)
        new_password = serializers.CharField(write_only=True, min_length=6)
        confirm_password = serializers.CharField(write_only=True)
    
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        
        if data["new_password"] != data["confirm_password"]:
            return Response(
                {"message": "New passwords do not match."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user_change_password(
                user=request.user,
                old_password=data["old_password"],
                new_password=data["new_password"]
            )
        except ValidationError as e:
            return Response(
                {"message": e.message},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(
            {"message": "Password changed successfully."},
            status=status.HTTP_200_OK
        )

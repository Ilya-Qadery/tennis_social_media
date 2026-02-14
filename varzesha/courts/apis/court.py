"""
Court APIs.
"""
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from varzesha.core.exceptions import ValidationError

from ..models import SurfaceType, Court
from ..selectors import (
    court_get,
    court_list,
    court_reviews_list,
    court_get_user_review,
)
from ..services import court_review_create


class CourtListApi(APIView):
    """API to list courts with filtering."""

    permission_classes = [AllowAny]

    class FilterSerializer(serializers.Serializer):
        city = serializers.CharField(required=False)
        surface_type = serializers.ChoiceField(
            choices=SurfaceType.choices, required=False
        )
        indoor = serializers.BooleanField(required=False)
        has_lights = serializers.BooleanField(required=False)
        min_price = serializers.IntegerField(required=False, min_value=0)
        max_price = serializers.IntegerField(required=False, min_value=0)
        min_rating = serializers.DecimalField(
            max_digits=2, decimal_places=1, required=False
        )
        has_parking = serializers.BooleanField(required=False)
        has_showers = serializers.BooleanField(required=False)

    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        name = serializers.CharField()
        city = serializers.CharField()
        address = serializers.CharField()
        surface_type = serializers.CharField()
        surface_type_display = serializers.CharField(source="get_surface_type_display")
        indoor = serializers.BooleanField()
        has_lights = serializers.BooleanField()
        price_per_hour = serializers.IntegerField()
        has_parking = serializers.BooleanField()
        has_showers = serializers.BooleanField()
        has_locker_room = serializers.BooleanField()
        has_equipment_rental = serializers.BooleanField()
        average_rating = serializers.DecimalField(max_digits=2, decimal_places=1)
        total_ratings = serializers.IntegerField()
        main_image = serializers.ImageField()
        lat = serializers.DecimalField(max_digits=9, decimal_places=6)
        lng = serializers.DecimalField(max_digits=9, decimal_places=6)

    def get(self, request):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        courts = court_list(**filters_serializer.validated_data)

        return Response(self.OutputSerializer(courts, many=True).data)


class CourtDetailApi(APIView):
    """API to get court details."""

    permission_classes = [AllowAny]

    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        name = serializers.CharField()
        description = serializers.CharField()
        city = serializers.CharField()
        address = serializers.CharField()
        lat = serializers.DecimalField(max_digits=9, decimal_places=6)
        lng = serializers.DecimalField(max_digits=9, decimal_places=6)
        surface_type = serializers.CharField()
        surface_type_display = serializers.CharField(source="get_surface_type_display")
        indoor = serializers.BooleanField()
        has_lights = serializers.BooleanField()
        price_per_hour = serializers.IntegerField()
        has_parking = serializers.BooleanField()
        has_showers = serializers.BooleanField()
        has_locker_room = serializers.BooleanField()
        has_equipment_rental = serializers.BooleanField()
        phone = serializers.CharField()
        website = serializers.CharField()
        average_rating = serializers.DecimalField(max_digits=2, decimal_places=1)
        total_ratings = serializers.IntegerField()
        main_image = serializers.ImageField()
        created_at = serializers.DateTimeField()

    def get(self, request, court_id):
        try:
            court = court_get(court_id=court_id)
        except Exception:
            return Response(
                {"message": "Court not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(self.OutputSerializer(court).data)


class CourtReviewListApi(APIView):
    """API to list and create court reviews."""

    # Default permission - safe for schema generation
    permission_classes = [AllowAny]

    class ReviewSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        user_name = serializers.CharField(source="user.full_name")
        rating = serializers.IntegerField()
        comment = serializers.CharField()
        created_at = serializers.DateTimeField()

    class CreateSerializer(serializers.Serializer):
        rating = serializers.IntegerField(min_value=1, max_value=5)
        comment = serializers.CharField(required=False, allow_blank=True)

    def get_permissions(self):
        """
        Override permissions based on request method.
        Safe to check self.request here because get_permissions() is called
        after request is initialized, unlike get_authenticators().
        """
        if self.request and self.request.method == "POST":
            return [IsAuthenticated()]
        return [AllowAny()]

    def get(self, request, court_id):
        reviews = court_reviews_list(court_id=court_id)
        return Response(self.ReviewSerializer(reviews, many=True).data)

    def post(self, request, court_id):
        try:
            court = court_get(court_id=court_id)
        except Exception:
            return Response(
                {"message": "Court not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check if user already reviewed
        existing = court_get_user_review(court_id=court_id, user=request.user)
        if existing:
            return Response(
                {"message": "You have already reviewed this court."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.CreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            review = court_review_create(
                court=court,
                user=request.user,
                **serializer.validated_data
            )
        except ValidationError as e:
            return Response(
                {"message": e.message},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            self.ReviewSerializer(review).data,
            status=status.HTTP_201_CREATED
        )


class CourtCitiesApi(APIView):
    """API to get list of cities with courts."""

    permission_classes = [AllowAny]

    def get(self, request):
        cities = Court.objects.filter(is_active=True).values_list(
            "city", flat=True
        ).distinct().order_by("city")

        return Response({"cities": list(cities)})
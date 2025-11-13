from rest_framework import serializers
from .models import (
    Airport,
    AirplaneType,
    Airplane,
    Route,
    Crew,
    Flight,
    Order,
)
from user.models import User


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("id", "name", "city", "code")


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ("id", "name", "capacity")


class AirplaneSerializer(serializers.ModelSerializer):
    airplane_type = AirplaneTypeSerializer(read_only=True)
    airplane_type_id = serializers.PrimaryKeyRelatedField(
        queryset=AirplaneType.objects.all(), source="airplane_type", write_only=True
    )

    class Meta:
        model = Airplane
        fields = ("id", "name", "airplane_type", "airplane_type_id")


class RouteSerializer(serializers.ModelSerializer):
    source = AirportSerializer(read_only=True)
    destination = AirportSerializer(read_only=True)
    source_id = serializers.PrimaryKeyRelatedField(
        queryset=Airport.objects.all(), source="source", write_only=True
    )
    destination_id = serializers.PrimaryKeyRelatedField(
        queryset=Airport.objects.all(), source="destination", write_only=True
    )

    class Meta:
        model = Route
        fields = (
            "id",
            "source",
            "destination",
            "source_id",
            "destination_id",
            "distance_km",
        )


class CrewSerializer(serializers.ModelSerializer):
    """Crew can have multiple members (Users)."""

    members = serializers.StringRelatedField(many=True, read_only=True)
    member_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        write_only=True,
        source="members",
    )

    class Meta:
        model = Crew
        fields = ("id", "name", "members", "member_ids")


class FlightSerializer(serializers.ModelSerializer):
    route = RouteSerializer(read_only=True)
    airplane = AirplaneSerializer(read_only=True)
    crew = CrewSerializer(read_only=True)

    route_id = serializers.PrimaryKeyRelatedField(
        queryset=Route.objects.all(), source="route", write_only=True
    )
    airplane_id = serializers.PrimaryKeyRelatedField(
        queryset=Airplane.objects.all(), source="airplane", write_only=True
    )
    crew_id = serializers.PrimaryKeyRelatedField(
        queryset=Crew.objects.all(), source="crew", write_only=True
    )

    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "crew",
            "route_id",
            "airplane_id",
            "crew_id",
            "departure_time",
            "arrival_time",
        )

class OrderSerializer(serializers.ModelSerializer):
    """Serializer for user orders."""

    user = serializers.StringRelatedField(read_only=True)
    flight = FlightSerializer(read_only=True)
    flight_id = serializers.PrimaryKeyRelatedField(
        queryset=Flight.objects.all(), source="flight", write_only=True
    )

    class Meta:
        model = Order
        fields = ("id", "user", "flight", "flight_id", "created_at")
        read_only_fields = ("id", "user", "created_at")

import pytest
from airport.models import (
    Airport,
    AirplaneType,
    Airplane,
    Route,
)


pytestmark = pytest.mark.django_db


def test_create_airport() -> None:
    airport = Airport.objects.create(name="Boryspil", city="Kyiv", code="KBP")
    assert airport.name == "Boryspil"
    assert airport.code == "KBP"


def test_create_airplane_type() -> None:
    airplane_type = AirplaneType.objects.create(name="Boeing 737", capacity=150)
    assert airplane_type.capacity == 150


def test_create_airplane_with_type() -> None:
    airplane_type = AirplaneType.objects.create(name="Boeing 777", capacity=300)
    airplane = Airplane.objects.create(name="TestPlane", airplane_type=airplane_type)
    assert airplane.airplane_type.name == "Boeing 777"


def test_create_route() -> None:
    src = Airport.objects.create(name="Lviv", city="Lviv", code="LWO")
    dst = Airport.objects.create(name="Warsaw", city="Warsaw", code="WAW")
    route = Route.objects.create(source=src, destination=dst, distance_km=700)
    assert route.source.code == "LWO"
    assert route.destination.city == "Warsaw"
    assert route.distance_km == 700

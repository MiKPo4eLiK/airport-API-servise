from airport.serializers import AirportSerializer
from airport.models import Airport


def test_airport_serializer() -> None:
    airport = Airport.objects.create(name="Odesa", city="Odesa", code="ODS")
    serializer = AirportSerializer(airport)
    data = serializer.data

    assert data["name"] == "Odesa"
    assert data["code"] == "ODS"
    assert set(data.keys()) == {"id", "name", "city", "code"}

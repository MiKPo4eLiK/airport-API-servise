import pytest
from rest_framework.test import APIClient
from airport.models import Airport
from django.urls import reverse

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client() -> object:
    return APIClient()


def test_airport_list_view(api_client) -> None:
    Airport.objects.create(name="Kharkiv", city="Kharkiv", code="HRK")
    url = reverse("airport-list")  # name pattern from DefaultRouter
    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["code"] == "HRK"


def test_airport_create_admin(api_client, django_user_model) -> None:
    """Only admin should be able to create an airport"""
    admin = django_user_model.objects.create_superuser(
        username="admin", email="admin@example.com", password="password123"
    )
    api_client.force_authenticate(admin)

    url = reverse("airport-list")
    payload = {"name": "Dnipro", "city": "Dnipro", "code": "DNK"}
    response = api_client.post(url, payload, format="json")

    assert response.status_code == 201
    assert Airport.objects.filter(code="DNK").exists()

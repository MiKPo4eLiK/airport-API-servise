import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestUserViewSet:
    def setup_method(self) -> None:
        self.client = APIClient()
        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="adminpass123",
        )
        self.user = User.objects.create_user(
            username="user1",
            email="user1@example.com",
            password="userpass123",
        )

    def test_user_list_requires_auth(self) -> None:
        url = reverse("user-list")
        response = self.client.get(url)
        assert response.status_code == 401

    def test_user_list_admin_access(self) -> None:
        self.client.force_authenticate(self.admin)
        url = reverse("user-list")
        response = self.client.get(url)
        assert response.status_code == 200
        assert isinstance(response.data, list) or "results" in response.data

    def test_user_detail_self_access(self) -> None:
        self.client.force_authenticate(self.user)
        url = reverse("user-detail", args=[self.user.id])
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.data["username"] == self.user.username

    def test_user_detail_denied_for_other_users(self) -> None:
        self.client.force_authenticate(self.user)
        url = reverse("user-detail", args=[self.admin.id])
        response = self.client.get(url)
        assert response.status_code in (403, 404)

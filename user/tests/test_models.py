import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestUserModel:
    def test_create_user(self) -> None:
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            first_name="John",
            last_name="Doe",
        )

        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.check_password("testpass123")
        assert not user.is_staff

    def test_create_superuser(self) -> None:
        admin = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="adminpass123",
        )

        assert admin.is_staff
        assert admin.is_superuser
        assert admin.email == "admin@example.com"
        assert admin.check_password("adminpass123")

    def test_str_representation(self) -> None:
        user = User.objects.create_user(
            username="cooluser",
            email="cool@example.com",
            password="12345",
        )
        assert str(user) == "cooluser (cool@example.com)"

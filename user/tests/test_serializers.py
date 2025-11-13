import pytest
from user.serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_user_serializer_output() -> None:
    user = User.objects.create_user(
        username="tester",
        email="tester@example.com",
        password="password123",
        first_name="Jane",
        last_name="Doe",
    )

    serializer = UserSerializer(user)
    data = serializer.data

    assert data["username"] == "tester"
    assert data["email"] == "tester@example.com"
    assert "password" not in data

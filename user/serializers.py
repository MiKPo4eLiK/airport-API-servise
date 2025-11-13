from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Base serializer for User model."""

    class Meta:
        model = User
        fields = ("id", "username", "email", "is_pilot", "is_staff_member")


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "is_pilot", "is_staff_member")

    def create(self, validated_data) -> object:
        request = self.context.get("request")

        if not request or not getattr(request.user, "is_staff", False):
            validated_data["is_staff_member"] = False

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            password=validated_data["password"],
        )
        user.is_pilot = validated_data.get("is_pilot", False)
        user.is_staff_member = validated_data.get("is_staff_member", False)
        user.is_active = True
        user.save()
        return user

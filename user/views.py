from rest_framework import permissions, viewsets
from django.contrib.auth import get_user_model
from rest_framework.serializers import Serializer

from .serializers import UserSerializer, UserCreateSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for working with users.
    - Admin can see everyone and create any users.
    - Regular user can only view themselves.
    - Registration of new users is open to everyone.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self) -> list[permissions.BasePermission]:
        """Different permissions for different actions."""
        if self.action == "create":
            return [permissions.AllowAny()]
        elif self.action in ["list", "destroy"]:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def get_serializer_class(self) -> type[Serializer]:
        """Return the desired serializer depending on the action."""
        if self.action == "create":
            return UserCreateSerializer
        return UserSerializer

    def get_queryset(self) -> object:
        """Admin sees everyone, user sees only themselves."""
        user = self.request.user
        if user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=user.id)

    def perform_create(self, serializer) -> None:
        """
        If a user is not an administrator, they cannot create staff users.
        """
        request = self.request
        if not request.user.is_staff:
            serializer.validated_data["is_staff_member"] = False
        serializer.save()

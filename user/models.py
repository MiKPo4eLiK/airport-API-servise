from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model for the airport system."""

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    is_pilot = models.BooleanField(default=False)
    is_staff_member = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.username} ({self.email})"

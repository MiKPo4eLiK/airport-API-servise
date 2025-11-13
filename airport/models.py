from django.db import models
from django.conf import settings


class Airport(models.Model):
    """Represents an airport."""

    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.name} ({self.city}, {self.country})"


class Crew(models.Model):
    """Represents a crew member."""

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    position = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} - {self.position}"


class AirplaneType(models.Model):
    """Represents a type of airplane (e.g., Boeing 737)."""

    name = models.CharField(max_length=100)

    def __str__(self) -> object:
        return self.name


class Airplane(models.Model):
    """Represents an airplane."""

    name = models.CharField(max_length=100)
    rows = models.PositiveIntegerField()
    seats_in_row = models.PositiveIntegerField()
    airplane_type = models.ForeignKey(AirplaneType, on_delete=models.CASCADE, related_name="airplanes")

    def __str__(self) -> str:
        return f"{self.name} ({self.airplane_type})"

    @property
    def capacity(self) -> str:
        """Return total number of seats."""
        return self.rows * self.seats_in_row


class Route(models.Model):
    """Represents a flight route from one airport to another."""

    source = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")
    distance = models.PositiveIntegerField(help_text="Distance in km")

    def __str__(self) -> str:
        return f"{self.source} → {self.destination}"


class Flight(models.Model):
    """Represents a scheduled flight."""

    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="flights")
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE, related_name="flights")
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crew = models.ManyToManyField(Crew, related_name="flights")

    def __str__(self) -> str:
        return f"Flight {self.route} ({self.departure_time:%Y-%m-%d %H:%M})"


class Order(models.Model):
    """Represents a booking order made by a user."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Order {self.id} by {self.user}"  # type: ignore[attr-defined]


class Ticket(models.Model):
    """Represents a booked seat on a flight."""

    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="tickets")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="tickets")

    def __str__(self) -> str:
        return f"Seat {self.row}-{self.seat} on {self.flight}"

    class Meta:
        unique_together = ("flight", "row", "seat")

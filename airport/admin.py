from django.contrib import admin
from .models import (
    Airport,
    AirplaneType,
    Airplane,
    Route,
    Crew,
    Flight,
)


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "show_code")
    search_fields = ("name", "city")

    def show_code(self, obj) -> object:
        """Show airport code if exists."""
        return getattr(obj, "code", getattr(obj, "iata_code", "—"))
    show_code.short_description = "Code"


@admin.register(AirplaneType)
class AirplaneTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "show_capacity")
    search_fields = ("name",)

    def show_capacity(self, obj) -> object:
        """Show airplane capacity if exists."""
        return getattr(obj, "capacity", getattr(obj, "seats", "—"))
    show_capacity.short_description = "Capacity"


@admin.register(Airplane)
class AirplaneAdmin(admin.ModelAdmin):
    list_display = ("name", "airplane_type")
    search_fields = ("name",)
    list_filter = ("airplane_type",)


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ("source", "destination", "show_distance")
    search_fields = ("source__name", "destination__name")
    list_filter = ("source", "destination")

    def show_distance(self, obj) -> object:
        """Show distance in km if exists."""
        return getattr(obj, "distance_km", getattr(obj, "distance", "—"))
    show_distance.short_description = "Distance (km)"


@admin.register(Crew)
class CrewAdmin(admin.ModelAdmin):
    list_display = ("show_name", "show_members_count")
    search_fields = ("name",)

    def show_name(self, obj) -> object:
        return getattr(obj, "name", str(obj))
    show_name.short_description = "Crew Name"

    def show_members_count(self, obj) -> object:
        members = getattr(obj, "members", None)
        if members is None:
            return "—"
        try:
            return members.count()
        except Exception:
            return len(members) if hasattr(members, "__len__") else "—"
    show_members_count.short_description = "Members Count"


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ("route", "airplane", "show_crew", "departure_time", "arrival_time")
    list_filter = ("route", "airplane")
    search_fields = ("route__source__name", "route__destination__name")

    def show_crew(self, obj) -> object:
        """Display crew members as comma-separated string."""
        crew = getattr(obj, "crew", None)
        if crew is None:
            return "—"
        members = getattr(crew, "members", None)
        if members is None:
            return str(crew)
        try:
            return ", ".join(str(m) for m in members.all())
        except Exception:
            return "—"
    show_crew.short_description = "Crew"

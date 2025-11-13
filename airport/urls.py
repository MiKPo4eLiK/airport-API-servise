from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("airports", views.AirportViewSet)
router.register("flights", views.FlightViewSet)
router.register("orders", views.OrderViewSet, basename="order")

urlpatterns = [
    path("", include(router.urls)),
]

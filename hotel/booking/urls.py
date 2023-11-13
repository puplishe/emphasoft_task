from django.urls import path, include
from .views import ReservationViewSet
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'reservation', ReservationViewSet)

urlpatterns = [
    path('', include(router.urls))
]
from django.urls import path, include
from .views import RoomListApiView
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'rooms', RoomListApiView)

urlpatterns = [
    path('', include(router.urls))
]
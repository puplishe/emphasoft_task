from django.urls import path, include
from .views import RoomListApiView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'rooms', RoomListApiView)

urlpatterns = [
    path('', include(router.urls))
]
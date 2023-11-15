from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets

from .filters import RoomFilter
from .models import Room
from .serializers import RoomSerializer


class RoomListApiView(viewsets.ModelViewSet):
    """
    API endpoint for managing rooms.

    list:
    Get a list of all rooms.

    create:
    Create a new room. Access to staff only.

    retrieve:
    Get details of a specific room. Access to staff only.

    update:
    Update details of a specific room. Access to staff only.

    partial_update:
    Partially update details of a specific room. Access to staff only.

    destroy:
    Delete a room. Access to staff only.

    """
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = []
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = RoomFilter
    ordering_fields = ['price_per_night', 'capacity']
    ordering = ['name']

    def get_permissions(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            self.permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
        return super().get_permissions()

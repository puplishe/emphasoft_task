from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Reservation, Room
from .serializers import ReservationSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing reservations.

    list:
    Get a list of all reservations.

    create:
    Create a new reservation.

    retrieve:
    Get details of a specific reservation.

    update:
    Update details of a specific reservation.

    partial_update:
    Partially update details of a specific reservation.

    destroy:
    Cancel a reservation.

    get_user_reservations:
    Get a list of reservations for the authenticated user.
    """
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request: Request) -> JsonResponse:
        """
        Create a new reservation.

        Example Request Body:
        {
            "room": 1,
            "check_in": "2023-01-01",
            "check_out": "2023-01-02"
        }

        Example Response:
        {
            "message": "Room reserved successfully."
        }
        """
        room_id: int | None = request.data.get('room')
        check_in_str: str | None = request.data.get('check_in')
        check_out_str: str | None = request.data.get('check_out')

        if not (room_id and check_in_str and check_out_str):
            return Response({'message': 'Invalid request. Make sure all required fields are provided.'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            check_in = datetime.strptime(check_in_str, '%Y-%m-%d').date()
            check_out = datetime.strptime(check_out_str, '%Y-%m-%d').date()

            room: Room = get_object_or_404(Room, pk=room_id)

            existing_reservations: list[Reservation] = Reservation.objects.filter(room=room)
            for reservation in existing_reservations:
                if check_in <= reservation.check_out and check_out >= reservation.check_in:
                    return Response({'message': 'Room not available for the selected dates.'},
                                    status=status.HTTP_400_BAD_REQUEST)

            reservation: Reservation = Reservation.objects.create(
                user=request.user,
                room=room,
                check_in=check_in,
                check_out=check_out
            )

            return Response({'message': 'Room reserved successfully.'}, status=status.HTTP_201_CREATED)

        except Room.DoesNotExist:
            return Response({'message': 'Room not found.'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'], url_path='user-reservations')
    def get_user_reservations(self, request: Request) -> JsonResponse:
        """
        Get a list of reservations for the authenticated user.
        """
        reservations: list[Reservation] = Reservation.objects.filter(user=request.user)
        serializer: ReservationSerializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request: Request, *args, **kwargs) -> JsonResponse:
        """
        Cancel a reservation.
        """
        instance: Reservation = self.get_object()
        if instance.user == request.user:
            self.perform_destroy(instance)
            return Response({'message': 'Reservation canceled'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'You are not authorized to cancel this reservation.'},
                            status=status.HTTP_403_FORBIDDEN)

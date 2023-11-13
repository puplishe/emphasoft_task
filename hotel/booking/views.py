from django.shortcuts import render

# Create your views here.
from room.models import Room
from rest_framework import viewsets, status
from .models import Reservation
from .serializers import ReservationSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]
    def create(self, request):
        # Получите данные из запроса (комната, даты, пользователь и т. д.)
        room_id = request.data.get('room')
        check_in = datetime.strptime(request.data.get('check_in'), "%Y-%m-%d").date()
        check_out = datetime.strptime(request.data.get('check_out'), "%Y-%m-%d").date()
        user = request.user

        try:
            room = Room.objects.get(pk=room_id)

            # Проверьте доступность комнаты для указанных дат
            existing_reservations = Reservation.objects.filter(room=room)
            for reservation in existing_reservations:
                if check_in <= reservation.check_out and check_out >= reservation.check_in:
                    return Response({'message': 'Room not available for the selected dates.'}, status=status.HTTP_400_BAD_REQUEST)

            # Если комната доступна, создайте бронь
            reservation = Reservation.objects.create(
                user=user,
                room=room,
                check_in=check_in,
                check_out=check_out
            )

            return Response({'message': 'Room reserved successfully.'}, status=status.HTTP_201_CREATED)

        except Room.DoesNotExist:
            return Response({'message': 'Room not found.'}, status=status.HTTP_404_NOT_FOUND)
    def retrieve(self, request, *args, **kwargs):
        reservations = Reservation.objects.filter(user=request.user)
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user == request.user:
            self.perform_destroy(instance)
            return Response({'message': 'Reservation canceled'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'You are not authorized to cancel this reservation.'}, status=status.HTTP_403_FORBIDDEN)

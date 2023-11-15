from datetime import timedelta
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from room.models import Room
from .models import Reservation
from django.contrib.auth.models import User



class ReservationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.superuser = User.objects.create_superuser(username='admin', password='adminpassword')
        self.room = Room.objects.create(name='Test Room', price_per_night='100.00', capacity=2)
        self.valid_reservation_data = {
            'room': self.room.id,
            'check_in': '2023-11-01',
            'check_out': '2023-11-05'
        }

    def test_user_can_reserve_room(self):
        self.client.force_login(self.user)
        url = reverse('reservation-list')
        response = self.client.post(url, data=self.valid_reservation_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reservation.objects.count(), 1)
        reservation = Reservation.objects.first()
        self.assertEqual(reservation.user, self.user)
        self.assertEqual(reservation.room, self.room)

    def test_reservation_cancellation_by_user(self):
        self.client.force_login(self.user)
        reservation = Reservation.objects.create(user=self.user, room=self.room,
                                                 check_in='2023-11-01', check_out='2023-11-05')
        url = reverse('reservation-detail', args=[reservation.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Reservation.objects.count(), 0)

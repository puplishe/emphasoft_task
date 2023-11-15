from datetime import datetime, timedelta

from booking.models import Reservation
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Room


class RoomFilterTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_login(self.user)
        self.room_1 = Room.objects.create(name='Room 1', price_per_night='100.00', capacity=1)
        self.room_2 = Room.objects.create(name='Room 2', price_per_night='150.00', capacity=3)
        self.room_3 = Room.objects.create(name='Room 3', price_per_night='120.00', capacity=2)
        self.reservation_1 = Reservation.objects.create(
            user=self.user, room=self.room_1, check_in=datetime.today(), check_out=datetime.today() + timedelta(days=5)
        )

    def test_filter_rooms_by_capacity(self):
        url = reverse('room-list')
        response = self.client.get(url, {'capacity': 2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_rooms_by_price(self):
        url = reverse('room-list')
        response = self.client.get(url, {'max_price': 130.00})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_sort_rooms_by_price(self):
        url = reverse('room-list')
        response = self.client.get(url, {'ordering': 'price_per_night'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['price_per_night'], '100.00')

    def test_search_available_rooms(self):
        url = reverse('room-list')
        check_in = (datetime.today()).strftime('%Y-%m-%d')
        check_out = (datetime.today() + timedelta(days=5)).strftime('%Y-%m-%d')
        response = self.client.get(url, {'check_in': check_in, 'check_out': check_out})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

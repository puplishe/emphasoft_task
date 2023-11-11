from django.shortcuts import render
from rest_framework import generics
from serializers import RoomSerializer
from models import Room
# Create your views here.

class RoomListApiView(generics.ListAPIView):
    serializer_class = RoomSerializer

    def get_queryset(self):
        
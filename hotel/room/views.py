from django.shortcuts import render
from rest_framework import generics, viewsets
from .serializers import RoomSerializer
from .models import Room
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import date
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .filters import RoomFilter
# Create your views here.

class RoomListApiView(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = []
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = RoomFilter
    ordering_fields = ['price_per_night', 'capacity']
    ordering = ['name']
    
    
    
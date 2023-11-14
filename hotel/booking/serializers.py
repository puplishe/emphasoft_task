from rest_framework import serializers
from .models import Reservation

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id','user', 'room', 'check_in', 'check_out']
        read_only_fields = ['user']
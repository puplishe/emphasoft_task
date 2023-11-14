from django.db import models
from django.contrib.auth.models import User
from room.models import Room
# Create your models here.
class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    def __str__(self):
        return f'Reservation {self.id} of {self.room} by user:{self.user}'
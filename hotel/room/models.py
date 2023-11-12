from django.db import models

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=100)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.PositiveIntegerField()
    booked = models.BooleanField(default=False)

    def cancel_booking(self):
        self.booked = False
        self.save()
        
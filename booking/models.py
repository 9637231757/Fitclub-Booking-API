from django.db import models

# Create your models here.
from django.db import models
from django.utils.timezone import now

class FitnessClass(models.Model):
    name = models.CharField(max_length=50)
    datetime = models.DateTimeField()
    instructor = models.CharField(max_length=50)
    total_slots = models.PositiveIntegerField()
    available_slots = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} at {self.datetime}"

class Booking(models.Model):
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client_name} -> {self.fitness_class.name}"

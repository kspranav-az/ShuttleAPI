from django.db import models

class Device(models.Model):
    device_id = models.CharField(max_length=255, unique=True)  # Unique device identifier
    name = models.CharField(max_length=255, blank=True)  # Optional name for the device

class LocationUpdate(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)  # Time of the update
    latitude = models.FloatField()
    longitude = models.FloatField()
    altitude = models.FloatField(null=True, blank=True)  # Optional altitude
    accuracy = models.FloatField(null=True, blank=True)  # Optional accuracy

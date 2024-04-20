from rest_framework import serializers
from .models import Device, LocationUpdate

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'  # Include all fields for Device

class LocationUpdateSerializer(serializers.ModelSerializer):
    device = serializers.PrimaryKeyRelatedField(queryset=Device.objects.all())  # Validate against existing devices
    class Meta:
        model = LocationUpdate
        fields = '__all__'  # Include all fields for LocationUpdate

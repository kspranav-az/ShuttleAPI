from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Device
# from .models import LocationUpdate, Device
from .serializers import LocationUpdateSerializer, DeviceSerializer

class LocationUpdateView(APIView):
    def post(self, request):
        serializer = LocationUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(device = Device.objects.filter(device_id=request.data.get("device")).first())
            return Response({'message': 'Location update saved successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeviceView(APIView):
    def post(self, request):
        serializer = DeviceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response({'message': 'Device created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

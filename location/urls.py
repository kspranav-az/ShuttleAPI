from django.urls import path
from .views import LocationUpdateView , DeviceView

urlpatterns = [
    path('update/', LocationUpdateView.as_view(), name='location_update'),
    path('device/',DeviceView.as_view(),name='device')
]

from rest_framework import serializers
from location.models import Location, Status

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['name', 'description', 'moderator', 'slug']

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['activity', 'description', 'open_date', 'close_date', 'location', 'volunteer']
from rest_framework import serializers
from location.models import Location, Status

class LocationSerializer(serializers.HyperlinkedModelSerializer):
    moderator = serializers.ReadOnlyField(source='moderator.username')
    statuses = serializers.RelatedField(many=True, queryset=Status.objects.all())

    class Meta:
        model = Location
        fields = ['name', 'description', 'moderator', 'slug']

class StatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Status
        fields = ['activity', 'description', 'open_date', 'close_date', 'location', 'volunteer']

from rest_framework import serializers
from django.contrib.auth.models import User

from location.models import Location

class UserSerializer(serializers.HyperlinkedModelSerializer):
    location_moderator = serializers.HyperlinkedRelatedField(many=True, view_name='location-detail', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'location_moderator']
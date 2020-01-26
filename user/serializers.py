from rest_framework import serializers
from django.contrib.auth.models import User

from location.models import Location

class UserSerializer(serializers.HyperlinkedModelSerializer):
    location_moderator = serializers.HyperlinkedRelatedField(many=True, view_name='locations-detail', lookup_field='slug', lookup_url_kwarg='slug', read_only=True)

    class Meta:
        model = User
        fields = ['username', 'location_moderator', 'password', 'email']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import ValidationError
from geopy.distance import geodesic

from location.models import Location, Status
from location.permissions import IsModeratorOrReadOnly, IsVolunteerOrReadOnly
from location.serializers import LocationSerializer, StatusSerializer
from location.utils import get_near_localities

class LocationList(generics.ListCreateAPIView):
    """
    Return a list of all locations
    """
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(moderator=self.request.user)

    def get_queryset(self):
        nearlon = self.request.query_params.get('nearlon', None)
        nearlat = self.request.query_params.get('nearlat', None)
        nearcount = self.request.query_params.get('nearcount', 6)
        if nearlon is not None and nearlat is not None:

            try:
                user_location = (float(nearlat), float(nearlon))
                nearcount = int(nearcount)

            except ValueError:
                raise ValidationError(detail="""Invalid parameters, 
                                                'nearlat' should be latitude in radians, 
                                                'nearlon' should be longitude in radians,
                                                'nearcount' should be an integer""")
            weighted_locations = {}

            for location in Location.objects.all():
                distance = geodesic((location.latitude, location.longitude), user_location).km
                weighted_locations[distance] = location

            choice = sorted(list(weighted_locations.keys()))[:nearcount]
            queryset = []

            for key in choice:
                queryset.append(weighted_locations[key])

            return queryset

class LocationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsModeratorOrReadOnly]
    lookup_field = 'slug'

class StatusDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StatusSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsVolunteerOrReadOnly]
    queryset = Status.objects.all()

class StatusList(generics.ListCreateAPIView):
    serializer_class = StatusSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsVolunteerOrReadOnly]

    def get_queryset(self):
        location = Location.objects.get(slug=self.kwargs['slug'])
        return Status.objects.filter(location=location)

    def perform_create(self, serializer):
        location = Location.objects.get(slug=self.kwargs['slug'])
        self.check_object_permissions(self.request, location)
        serializer.save(location=location)

"""
A view with which the user can create a new location
:return: Return the location creation template or a redirection to
        new location detail page.
"""



"""
Allow user to send a volunteering request to the location moderator.

:param slug: Slug of the location
:return: Redirect to the updated location detail page
"""


"""
Allow moderator and volunteers to open a location by adding a status.

:param slug: Slug for the location
:return: Should return status creation form, or create a new status and
redirect to location detail view.
"""


"""
Allow moderator and volunteers to close a status.

:param slug: Slug for the location
:return: A redirection to location detail view
"""


"""
Redirect user to location selected in search field.

:return: A redirection to location detail view
"""


"""
Allow moderator to edit location information such as name and description

:param slug: Slug for the location
"""

"""
Allow moderator to delete location

:param slug: Slug for the location
"""

from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.http import Http404

from location.models import Location, Status
from location.permissions import IsModeratorOrReadOnly, IsVolunteerOrReadOnly
from location.serializers import LocationSerializer, StatusSerializer


class LocationList(generics.ListCreateAPIView):
    """
    Return a list of all locations
    """
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(moderator=self.request.user)

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

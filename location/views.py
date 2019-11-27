from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from django.http import Http404

from location.models import Location, Status
from location.serializers import LocationSerializer

class LocationList(APIView):
    """
    List all locations, or create a new one
    """

    def get(self, request, format=None):
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LocationDetail(APIView):
    """
    Retrieve, update or delete location instance
    """
    def get_location(self, slug):
        try:
            return Location.objects.get(slug=slug)
        except:
            raise Http404

    def get(self, request, slug, format=None):
        location = self.get_location(slug)
        serializer = LocationSerializer(location)
        return Response(serializer.data)

    def put(self, request, slug, format=None):
        location = self.get_location(slug)
        serializer = LocationSerializer(location, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug, format=None):
        location = self.get_location(slug)
        location.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

"""
Views that return main public informations about a given location
:param slug: Slug for the location
:return: Should return a different template whether user is logged or not.
        With user logged, various volunteer/moderator related data are
        sent in template context.
"""

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

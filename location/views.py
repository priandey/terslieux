from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status

from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from location.models import Location, Status
from location.permissions import IsModeratorOrReadOnly, IsVolunteerOrReadOnly
from location.serializers import LocationSerializer, StatusSerializer


class LocationViewSet(viewsets.ModelViewSet):
    """
    Provide 'list', 'create', 'retrieve' actions
    """
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    lookup_field = 'slug'
    permissions = [permissions.IsAuthenticatedOrReadOnly,
                   IsModeratorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(moderator=self.request.user)

class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permissions = [permissions.IsAuthenticatedOrReadOnly]

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

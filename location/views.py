from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import ValidationError
from geopy.distance import geodesic

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

    def get_queryset(self):
        queryset = []
        origin = self.request.query_params.get('origin', default='geolocated')

        if origin == 'geolocated':
            queryset = self.get_by_geolocation()

        elif origin == 'searchbar':
            queryset = self.get_by_filtering()

        return queryset

    def get_by_geolocation(self):
        ''' Get locations near coordinates '''
        result = []
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

            for key in choice:
                result.append(weighted_locations[key])
        # TODO : Queryset may be always empty, well check emptiness conditions
        return result

    def get_by_filtering(self):
        result = []

        return result


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

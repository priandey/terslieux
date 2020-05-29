import requests

from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
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
        search_type = self.request.query_params.get('search_type', default='name')

        if origin == 'geolocated':
            queryset = self.get_by_geolocation()

        elif origin == 'searchbar':
            if search_type == "name":
                queryset = self.get_by_name()

            elif search_type == "address":
                queryset = self.get_by_address()

        return queryset

    def get_by_geolocation(self, nearlon=False, nearlat=False, nearcount=False):
        ''' Get locations near coordinates '''
        result = []
        if not nearlon or not nearlat or not nearcount:
            nearlon = self.request.query_params.get('nearlon', False)
            nearlat = self.request.query_params.get('nearlat', False)
            nearcount = self.request.query_params.get('result_count', 6)

        if nearlon and nearlat:
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
        return result

    def get_by_name(self):
        """
        TODO : Result count not supported
        :return:
        """
        result = []
        search_terms = self.request.query_params.get('terms', None)

        if search_terms is not None:
            parsed_terms = search_terms.split(' ')
            for term in parsed_terms:
                for location in Location.objects.filter(name__icontains=term):
                    result.append(location)
        return result

    def get_by_address(self):
        """
        TODO : This could need the reusable coord extractor that should arrive in location.models.LocationManager
        :return:
        """
        result = []
        payload = {
            "q": self.request.query_params.get('terms', default=None),
            "limit": 1
        }
        result_count = self.request.query_params.get('result_count', default=10)
        r = requests.get("https://api-adresse.data.gouv.fr/search/", params=payload)
        r = r.json()
        try:
            if r["features"]:
                cursor = r["features"][0]
                longitude = cursor["geometry"]["coordinates"][0]
                latitude = cursor["geometry"]["coordinates"][1]
                result = self.get_by_geolocation(nearlon=longitude, nearlat=latitude, nearcount=result_count)
                print(cursor)
        except KeyError as e:
            print(f'Key error : r[{e}] not found')

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

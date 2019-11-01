from django.shortcuts import render

from user.models import CustomUser
from location.models import Location, Status

def home(request):
    locations = Location.objects.all()
    opened_locations = []
    for location in locations :
        if location.status.last().is_opened:
            opened_locations.append(location)
    return render(request, "home/index.html", locals())

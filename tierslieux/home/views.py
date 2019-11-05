from django.shortcuts import render

from location.models import Location, Status

def home(request):
    locations = Location.objects.all()
    opened_locations = []
    for location in locations:
        last_status = location.status.last()
        if last_status is not None:
            if last_status.is_opened:
                opened_locations.append(location)
    return render(request, "home/index.html", locals())

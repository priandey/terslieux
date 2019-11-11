from django.shortcuts import render
from django.http import JsonResponse

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


def autocomplete(request):
    term = request.GET['term']
    location_propositions = []
    limit = 15
    incr = 0

    for location in Location.objects.filter(name__contains=term):
        location_propositions.append(location.name)
        incr += 1
        if incr >= limit:
            break

    return JsonResponse(location_propositions, safe=False)

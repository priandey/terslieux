from django.shortcuts import render
from django.http import HttpResponseForbidden

from location.models import Location, VolunteerBase

def moderator_pannel(request):
    locations = Location.objects.filter(moderator=request.user)
    return render(request, "moderator/moderator_pannel.html", locals())

def volunteers(request, slug):
    location = Location.objects.get(slug=slug)
    if location.moderator == request.user:
        volunteers = location.volunteerbase_set.all()
        validated = list()
        pending = list()
        for volunteer in volunteers:
            if volunteer.volunteering_request.validated:
                validated.append(volunteer)
            else:
                pending.append(volunteer)
        response = render(request, "moderator/volunteers.html", locals())
    else:
        response = HttpResponseForbidden()
    return response

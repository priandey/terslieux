from django.shortcuts import render
from django.http import HttpResponseForbidden, HttpResponseRedirect

from location.models import Location, VolunteerBase, VolunteeringRequest

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

def change_vol_status(request, slug, req_pk, status):
    location = Location.objects.get(slug=slug)
    if location.moderator == request.user:
        if status == "validated":
            req = VolunteeringRequest.objects.get(pk=req_pk)
            req.validated = True
            req.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

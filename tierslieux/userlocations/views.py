from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from location.models import VolunteerBase, VolunteeringRequest

@login_required(login_url='/user/login/')
def locations(request):
    volunteerbase = VolunteerBase.objects.filter(volunteer=request.user)
    return render(request, 'userlocations/locations.html', locals())

def accept_volunteering(request, pk):
    req = VolunteeringRequest.objects.get(pk=pk)
    req.validated = True
    req.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from .models import UserFavorite
from location.models import VolunteerBase, VolunteeringRequest, Location, Status

@login_required(login_url='/user/login/')
def locations(request):
    volunteerbase = VolunteerBase.objects.filter(volunteer=request.user)
    favorites = UserFavorite.objects.filter(user=request.user)
    moderated = request.user.location.all()
    return render(request, 'userlocations/locations.html', locals())

@login_required(login_url='user/login/')
def add_favorite(request, slug):
    location = Location.objects.get(slug=slug)
    user = request.user
    new_fav = UserFavorite.objects.create(
            user=user,
            location=location,
    )
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def accept_volunteering(request, pk):
    req = VolunteeringRequest.objects.get(pk=pk)
    req.validated = True
    req.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

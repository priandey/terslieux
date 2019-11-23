from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .models import UserFavorite
from location.models import VolunteerBase, VolunteeringRequest, Location, Status


@login_required(login_url='/user/login/')
def locations(request):
    """
    Return location datas linked to the user
    """
    volunteerbase = VolunteerBase.objects.filter(volunteer=request.user)
    favorites = UserFavorite.objects.filter(user=request.user)
    moderated = request.user.location.all()
    return render(request, 'userlocations/locations.html', locals())


@login_required(login_url='user/login/')
def add_favorite(request, slug):
    """
    Allow a user to add a location in his favorites
    :param slug: Slug for the location
    """
    location = Location.objects.get(slug=slug)
    user = request.user
    if not UserFavorite.objects.filter(user=user, location=location):
        UserFavorite.objects.create(
            user=user,
            location=location,
        )
        response = redirect('location', slug=slug)
    else:
        response = HttpResponseForbidden("Ce lieu est déjà dans vos favoris")
    return response


def accept_volunteering(request, pk):
    """
    Allow user to accep a volunteering request from a moderator
    :param pk: Primary key of the volunteering request
    """
    req = VolunteeringRequest.objects.get(pk=pk)
    if req.receiver == request.user:
        req.validated = True
        req.save()
        response = redirect('private_locations')
    else:
        response = HttpResponseForbidden("Cette requête ne vous a pas été envoyée")
    return response

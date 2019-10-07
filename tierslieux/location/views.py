from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError

from user.models import CustomUser

from .models import Location, VolunteerBase, VolunteeringRequest
from .forms import LocationForm

def location_detail(request, slug):
    location = Location.objects.get(slug=slug)
    if request.user.is_authenticated:
        user = request.user
        try:
            for entry in VolunteerBase.objects.filter(location=location):
                if user == entry.volunteer:
                    disclaimer = "Vous êtes bénévole sur ce lieu"
                else:
                    pass
        except user.models.Volunteer.DoesNotExist:
            print("There was an error DoesNotExist")

    return render(request, 'location/location_detail.html', locals())


@login_required(login_url='/user/login/')
def location_creation(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            new_location = form.save(commit=False)
            new_location.moderator = request.user
            new_location.save()
            return HttpResponseRedirect('/')
    else:
        form = LocationForm()
    return render(request, 'location/location_creation.html', locals())

@login_required(login_url='/user/login/')
def require_volunteering(request):
    if request.method == 'POST':
        print(request.POST)
        location = Location.objects.get(slug=request.POST['location'])
        comment = request.POST['comment']
        requesting_user = request.user
        moderator = location.moderator

        sent_request = VolunteeringRequest.objects.create(
                sender=requesting_user,
                receiver=moderator,
                comment=comment
        ) #Creating a new request

        VolunteerBase.objects.create(
                volunteer=requesting_user,
                location=location,
                is_active=False,
                volunteering_request=sent_request
        ) #Creating a new entry for the location in the volunteer base
        return redirect('location', slug=location.slug)

#TODO : location_edition view for moderator
#TODO : requesting to be volunteer upon a location for members
#TODO : status_declaration view for volunteer
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError

from user.models import Moderator, CustomUser, Volunteer

from .models import Location, VolunteerBase, VolunteeringRequest
from .forms import LocationForm

def location_detail(request, slug):
    location = Location.objects.get(slug=slug)
    if request.user.is_authenticated:
        user = request.user
        try:
            volunteer = Volunteer.objects.get(user=user)
            for entry in VolunteerBase.objects.filter(location=location):
                if volunteer == entry.volunteer:
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
            try:
                moderator = Moderator.objects.create(user=CustomUser.objects.get(pk=request.user.pk))
            except IntegrityError:
                moderator = Moderator.objects.get(user=request.user)
            new_location.moderator = moderator
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
        moderator = location.moderator.user

        volunteer = Volunteer.objects.create(user=requesting_user) #Creating a new Volunteer

        request = VolunteeringRequest.objects.create(
                sender=requesting_user,
                receiver=moderator,
                comment=comment
        ) #Creating a new request

        VolunteerBase.objects.create(
                volunteer=volunteer,
                location=location,
                is_active=False,
                volunteering_request=request
        ) #Creating a new entry for the location in the volunteer base
        return redirect('location', slug=location.slug)

#TODO : location_edition view for moderator
#TODO : requesting to be volunteer upon a location for members
#TODO : status_declaration view for volunteer
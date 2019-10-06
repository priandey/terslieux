from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError

from user.models import Moderator, CustomUser, Volunteer

from .models import Location, VolunteerBase
from .forms import LocationForm

def location_detail(request, slug):
    location = Location.objects.get(slug=slug)
    if request.user.is_authenticated:
        user = request.user
        try :
            volunteer = Volunteer.objects.filter(user=user)
            for entry in VolunteerBase.objects.filter(location=location):
                if volunteer == entry.volunteer:
                    disclaimer = "Vous êtes bénévole sur ce lieu"
                else :
                    pass
        except user.models.Volunteer.DoesNotExist:
            pass

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


#TODO : location_edition view for moderator
#TODO : requesting to be volunteer upon a location for members
#TODO : status_declaration view for volunteer

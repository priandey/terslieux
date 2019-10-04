from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError

from user.models import Moderator, CustomUser

from .models import Location
from .forms import LocationForm

def location_detail(request, slug):
    location = Location.objects.get(slug=slug)
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

#TODO : location_edition view for moderator
#TODO : requesting to be volunteer upon a location for members
#TODO : status_declaration view for volunteer

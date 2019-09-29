from django.http import HttpResponseRedirect
from django.shortcuts import render

from .models import Location
from .forms import LocationForm

def location_detail(request, slug):
    location = Location.objects.get(slug=slug)
    return render(request, 'location/location_detail.html', locals())

def location_creation(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = LocationForm()
    return render(request, 'location/location_creation.html', locals())
from django.shortcuts import render

from user.models import Moderator, Volunteer
from location.models import Location

def home(request):
    moderators = Moderator.objects.all()
    locations = Location.objects.all()
    return render(request, "home/index.html", locals())
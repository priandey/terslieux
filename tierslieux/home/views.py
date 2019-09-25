from django.shortcuts import render

from user.models import Moderator, Volunteer, CustomUser
from location.models import Location

def home(request):
    moderators = Moderator.objects.all()
    locations = Location.objects.all()
    members = CustomUser.objects.all()
    volunteers = Volunteer.objects.all()
    return render(request, "home/index.html", locals())
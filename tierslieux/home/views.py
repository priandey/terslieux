from django.shortcuts import render

from user.models import CustomUser
from location.models import Location

def home(request):
    locations = Location.objects.all()
    members = CustomUser.objects.all()
    return render(request, "home/index.html", locals())
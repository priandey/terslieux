from django.shortcuts import render

from user.models import Moderator
from location.models import Location, VolunteerBase

def moderator_pannel(request):
    locations = request.user.mod.get().location.all()
    return render(request, "moderator/moderator_pannel.html", locals())

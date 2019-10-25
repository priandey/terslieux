from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist

from location.models import Location, VolunteerBase, VolunteeringRequest
from user.models import CustomUser

def moderator_pannel(request):
    locations = Location.objects.filter(moderator=request.user)
    return render(request, "moderator/moderator_panel.html", locals())

def volunteers(request, slug):
    location = Location.objects.get(slug=slug)
    if location.moderator == request.user:
        volunteers = location.volunteerbase_set.all()
        validated = list()
        required_by_mod = list()
        required_by_vol = list()
        for volunteer in volunteers:
            if volunteer.volunteering_request.validated:
                validated.append(volunteer)
            elif volunteer.volunteering_request.validated == False:
                required_by_vol.append(volunteer)
            else:
                required_by_mod.append(volunteer)
        response = render(request, "moderator/volunteers.html", locals())
    else:
        response = HttpResponseForbidden()
    return response

def change_vol_status(request, slug, req_pk, status):
    location = Location.objects.get(slug=slug)
    if location.moderator == request.user:
        if status == "validated":
            req = VolunteeringRequest.objects.get(pk=req_pk)
            req.validated = True
            req.save()
            volunteer = req.volunteer_base.get()
            volunteer.is_active = True
            volunteer.save()
        elif status == "remove":
            req = VolunteeringRequest.objects.get(pk=req_pk)
            req.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def request_volunteer(request, slug): #TODO : Email activation à la création d'un compte bénévole
    location = Location.objects.get(slug=slug)
    if location.moderator == request.user:
        if request.method == 'POST':
            requesting_user = location.moderator
            try:
                receiver = CustomUser.objects.get(email=request.POST['email'])

                sent_request = VolunteeringRequest.objects.create(
                        sender=requesting_user,
                        receiver=receiver,
                )  # Creating a new request

                VolunteerBase.objects.create(
                        volunteer=receiver,
                        location=location,
                        is_active=False,
                        volunteering_request=sent_request
                )  # Creating a new entry for the location in the volunteer base
            except ObjectDoesNotExist:
                return render(request, 'moderator/new_user.html', locals())
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def mod_create_vol(request, slug):
    location = Location.objects.get(slug=slug)
    if location.moderator == request.user:
        if request.method == 'POST':
            requesting_user = location.moderator
            receiver = CustomUser.objects.create_user(request.POST['mail'], request.POST['password'])
            receiver.save()

            sent_request = VolunteeringRequest.objects.create(
                    sender=requesting_user,
                    receiver=receiver,
            )  # Creating a new request

            VolunteerBase.objects.create(
                    volunteer=receiver,
                    location=location,
                    is_active=False,
                    volunteering_request=sent_request
            )
    return redirect(to='volunteers_panel', slug=slug, permanent=True)
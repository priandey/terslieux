from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist

from location.models import Location, VolunteerBase, VolunteeringRequest
from user.models import CustomUser


def volunteers(request, slug):
    """
    Collect every volunteers linked to the location and sort them in :
        - validated (the volunteer is active and can open the location)
        - required_by_mod (A request has been sent from the moderator to a user)
        - required_by_vol (A request has been sent from a user to the moderator)

    :param slug: Slug for the location
    """
    location = Location.objects.get(slug=slug)
    if location.moderator == request.user:
        all_volunteers = location.volunteerbase_set.all()
        validated = list()
        required_by_mod = list()
        required_by_vol = list()
        for volunteer in all_volunteers:
            if volunteer.volunteering_request.validated:
                validated.append(volunteer)
            elif volunteer.volunteering_request.validated == False:
                required_by_vol.append(volunteer)
            else:
                required_by_mod.append(volunteer)
        response = render(request, "moderator/volunteers.html", locals())
    else:
        response = HttpResponseForbidden("Vous n'êtes pas modérateur de ce lieu")
    return response


def change_vol_status(request, slug, req_pk, status):
    """
    Allow moderator to validate a request from a user, or to remove a request.

    :param slug: Slug for the location
    :param req_pk: Primary key for the volunteering request
    :param status: Status user wish to put on the volunteering_request
    """
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
        response = redirect('volunteers_panel', slug=slug)
    else:
        response = HttpResponseForbidden()
    return response


def request_volunteer(request, slug):
    """
    Allow moderator to request volunteership to a user.
    If user does not exist in database, moderator is sent to create a user
    :param slug: Slug for the location
    """
    location = Location.objects.get(slug=slug)
    if location.moderator == request.user:
        if request.method == 'POST':
            requesting_user = location.moderator
            try:
                receiver = CustomUser.objects.get(username=request.POST['username'])

                sent_request = VolunteeringRequest.objects.create(
                        sender=requesting_user,
                        receiver=receiver,
                )  # Creating a new request

                VolunteerBase.objects.create(
                        volunteer=receiver,
                        location=location,
                        is_active=True,
                        volunteering_request=sent_request
                )  # Creating a new entry for the location in the volunteer base

                response = redirect('volunteers_panel', slug=slug)
            except ObjectDoesNotExist:
                username = request.POST['username']
                response = render(request, 'moderator/new_user.html', locals())
    else:
        response = HttpResponseForbidden("Vous n'êtes pas modérateur de ce lieu")

    return response


def mod_create_vol(request, slug):  # TODO : username activation < username backend + Change this into a usage of user signin form
    """
    Allow a moderator to create a new user.
    :param slug: Slug for the location
    """
    location = Location.objects.get(slug=slug)
    if location.moderator == request.user:
        if request.method == 'POST':
            requesting_user = location.moderator
            receiver = CustomUser.objects.create_user(request.POST['username'], request.POST['password'])
            receiver.save()

            sent_request = VolunteeringRequest.objects.create(
                    sender=requesting_user,
                    receiver=receiver,
            )  # Creating a new request

            VolunteerBase.objects.create(
                    volunteer=receiver,
                    location=location,
                    is_active=True,
                    volunteering_request=sent_request
            )
        response = redirect('volunteers_panel', slug=slug)
    else:
        response = HttpResponseForbidden("Vous n'êtes pas modérateur de ce lieu")
    return response

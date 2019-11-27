from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .models import UserFavorite
from location.models import VolunteerBase, VolunteeringRequest, Location, Status



"""
TODO: Return location datas linked to the user
"""



"""
Allow a user to add a location in his favorites
:param slug: Slug for the location
"""



"""
Allow user to accept a volunteering request from a moderator
:param pk: Primary key of the volunteering request
"""
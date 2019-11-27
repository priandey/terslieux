from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser
from django.db.utils import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from .forms import SigninForm, EditProfileForm
from .models import CustomUser


"""
    Sign in view
"""


"""
Log-in View
"""


"""
Logout view
"""



"""
Return user data
"""


"""
Allow user to change his password (and future account related data)
"""


"""
Allow user to delete his account.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser
from django.db.utils import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from .forms import SigninForm, EditProfileForm
from .models import CustomUser


def sign_in(request):
    """
        Sign in view
    """

    form = SigninForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        try:
            new_user = CustomUser.objects.create_user(username, password)
            new_user.save()
            if not isinstance(request.user, AnonymousUser):
                user = authenticate(request, username=username, password=password)
                login(request, user)
            return redirect('home')
        except IntegrityError:
            duplicate_username = True
    else:
        validForm = False

    return render(request, 'user/signin.html', locals())


def log_in(request):
    """
    Log-in View
    """

    form = SigninForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request=request, user=user)
            return redirect("private_locations")
        else:
            logged = False

    return render(request, 'user/login.html', locals())


def log_out(request):
    """
    Logout view
    """

    logout(request)
    return redirect("home")


@login_required(login_url='/user/login/')
def profile(request):
    """
    Return user data
    """
    return render(request, "user/userprofile.html", locals())


@login_required(login_url='/user/login/')
def edit_profile(request):
    """
    Allow user to change his password (and future account related data)
    """
    user = request.user
    if request.method == 'POST':
        form = EditProfileForm(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data['password'])
            user.save()
            response = redirect('userprofile')
        else:
            response = render(request, 'user/edit_profile.html', {
                'form': form,
                'error': True,
            })
    else:
        form = EditProfileForm()
        response = render(request, 'user/edit_profile.html', {'form': form})
    return response

@login_required(login_url='/user/login')
def delete_profile(request):
    """
    Allow user to delete his account.
    """
    if request.method == 'POST':
        user = request.user.pk
        logout(request)
        CustomUser.objects.get(pk=user).delete()
    return redirect('home', permanent=True)

from django.urls import path
from . import views

urlpatterns = [
    path('', views.locations, name='private_locations'),
    path('accept/<int:pk>', views.accept_volunteering, name='accept_vol')
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.locations, name='private_locations'),
    path('new_fav/<slug:slug>', views.add_favorite, name="new_fav"),
    path('accept/<int:pk>', views.accept_volunteering, name='accept_vol')
]
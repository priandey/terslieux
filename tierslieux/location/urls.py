from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.location_creation, name='create_loc'),
    path('<slug:slug>/', views.location_detail),
]
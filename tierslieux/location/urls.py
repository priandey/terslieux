from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.location_creation),
    path('<slug:slug>/', views.location_detail),
]
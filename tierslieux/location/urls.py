from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_location, name='search_location'),
    path('create/', views.location_creation, name='create_loc'),
    path('require/<slug:slug>', views.require_volunteering, name='require_volunteering'),
    path('<slug:slug>/', views.location_detail, name='location'),
    path('<slug:slug>/status', views.add_status, name='add_status'),
    path('<slug:slug>/close', views.close_status, name='close_status'),
]

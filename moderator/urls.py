from django.urls import path

from . import views

urlpatterns = [
    path('<slug:slug>/', views.volunteers, name='volunteers_panel'),
    path('<slug:slug>/create_vol', views.mod_create_vol, name='mod_create_vol'),
    path('<slug:slug>/<int:req_pk>/<str:status>', views.change_vol_status, name='validate'),
    path('<slug:slug>/new_vol/', views.request_volunteer, name='new_vol'),
]

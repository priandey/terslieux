"""tierslieux URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from . import views

urlpatterns = [
    path('', views.moderator_pannel, name='moderator_pannel'),
    path('<slug:slug>/', views.volunteers, name='volunteers_panel'),
    path('<slug:slug>/create_vol', views.mod_create_vol, name='mod_create_vol'),
    path('<slug:slug>/<int:req_pk>/<str:status>', views.change_vol_status, name='validate'),
    path('<slug:slug>/new_vol/', views.request_volunteer, name='new_vol'),
]

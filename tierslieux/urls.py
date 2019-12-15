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
from django.urls import path, include
from location.views import LocationList, LocationDetail, StatusDetail, StatusList
from user.views import UserList, UserDetail

urlpatterns = [
    path('locations/', LocationList.as_view(), name='locations-list'),
    path('locations/<slug:slug>', LocationDetail.as_view(), name='locations-detail'),
    path('locations/<slug:slug>/statuses', StatusList.as_view(), name='statuses-list'),
    path('statuses/<int:pk>', StatusDetail.as_view(), name='status-detail'),
    path('users/', UserList.as_view(), name='users-list'),
    path('users/<int:pk>', UserDetail.as_view(), name='users-detail'),
    path('api-auth/', include('rest_framework.urls')),
]


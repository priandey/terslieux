from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from location import views

urlpatterns = [
    path('', views.LocationList.as_view()),
    path('<slug:slug>/', views.LocationDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
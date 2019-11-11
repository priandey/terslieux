from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.sign_in, name='signin'),
    path('login/', views.log_in, name='login'),
    path('logout/', views.log_out, name="logout"),
    path('profile/', views.profile, name="userprofile"),
    path('editprofile/', views.edit_profile, name="edit_profile"),
    path('delprofile/', views.delete_profile, name='delete_profile')
]
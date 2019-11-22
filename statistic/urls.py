from django.urls import path

from . import views

urlpatterns = [
    path('<slug:slug>', views.generate_pdf, name='generate_pdf'),
]

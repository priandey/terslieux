from django.urls import path

from . import views

urlpatterns = [
    path('pdf/<slug:slug>', views.generate_pdf, name='generate_pdf'),
    path('csv/<slug:slug>', views.generate_csv, name='generate_csv'),
]

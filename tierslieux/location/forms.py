from django.forms import ModelForm
from .models import Location, Status

class LocationForm(ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'description', 'slug']

class StatusForm(ModelForm):
    class Meta:
        model = Status
        fields = ['activity',]
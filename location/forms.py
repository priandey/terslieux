from django import forms
from .models import Location, Status


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'description']
        widgets = {
            'name'       : forms.TextInput(attrs={
                'class'      : 'form-control',
                'placeholder': 'Nom du lieu'
            }),

            'description': forms.Textarea(attrs={
                'class'      : 'form-control',
                'placeholder': 'Une description du lieu',
                'rows'       : 4
            }),

        }

        labels = {
            'name'       : '',
            'description': '',
        }


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['activity', 'description']
        widgets = {
            'activity'   : forms.TextInput(attrs={
                'class'      : 'form-control',
                'placeholder': "Activité prévue durant l'ouverture"
            }),
            'description': forms.Textarea(attrs={
                'class'      : 'form-control',
                'placeholder': 'Des choses à préciser ?',
                'rows'       : 4,
            })
        }

        labels = {
            'activity'   : '',
            'description': ''
        }

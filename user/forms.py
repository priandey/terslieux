from django import forms

class SigninForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Votre Email'
    }), required=True, label='')
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'id': 'password',
        'class': 'form-control',
        'placeholder': 'Mot de passe'
    }), label='')

class EditProfileForm(forms.Form):
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'id': 'password',
        'class': 'form-control',
        'placeholder': 'Mot de passe'
    }), label='')

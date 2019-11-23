from django import forms


class SigninForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class'      : 'form-control',
        'placeholder': "Votre nom d'utilisateur"
    }), required=True, label='')
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'id'         : 'password',
        'class'      : 'form-control',
        'placeholder': 'Mot de passe'
    }), label='')


class EditProfileForm(forms.Form):
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'id'         : 'password',
        'class'      : 'form-control',
        'placeholder': 'Mot de passe'
    }), label='')

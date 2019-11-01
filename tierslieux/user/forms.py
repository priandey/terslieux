from django import forms

class SigninForm(forms.Form):
    email = forms.EmailField(label="Adresse E-mail", required=True)
    password = forms.CharField(label="Mot de passe", required=True, widget=forms.PasswordInput(attrs={'id':'password'}))

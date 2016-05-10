from django.contrib.auth.models import User
from master.models import UserProfile
from django import forms


class LoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {
            'email':  forms.TextInput(attrs={'class': 'w3-input w3-border w3-round-large email-field'}),
            'password': forms.PasswordInput(attrs={'class': 'w3-input w3-border w3-round-large password-field'}),
        }


class VerkoperForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w3-input w3-border w3-round-large partner-field', 'placeholder' : 'voornaam'}),
            'last_name': forms.TextInput(attrs={'class': 'w3-input w3-border w3-round-large partner-field', 'placeholder' : 'achternaam'}),
            'email': forms.TextInput(attrs={'class': 'w3-input w3-border w3-round-large partner-field', 'placeholder' : 'email'}),
        }


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['locatie', 'geslacht']
        widgets = {
            'locatie': forms.TextInput(attrs={'class': 'w3-input w3-border w3-round-large partner-field'}),
            'geslacht': forms.TextInput(attrs={'class': 'w3-input w3-border w3-round-large partner-field'}),
        }

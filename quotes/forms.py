# quotes/forms.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class QuoteRequestForm(forms.Form):
    name = forms.CharField(label='Your Name', max_length=100)
    email = forms.EmailField(label='Your Email')
    phone = forms.CharField(label='Your Phone Number', max_length=15)
    description = forms.CharField(label='Project Description', widget=forms.Textarea, max_length=1000)
    materials_needed = forms.CharField(label='Materials Needed', widget=forms.Textarea, max_length=1000)

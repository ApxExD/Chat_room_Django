from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from .models import Room

class RegisterForm(ModelForm):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.CharField(widget=forms.EmailInput)
    class Meta:
        model = User
        fields = ["username", "password", "email"]

class CreateRoom(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host']

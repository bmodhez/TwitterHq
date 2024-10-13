from django import forms
from .models import tweet
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class Tweetform(forms.ModelForm):  
    class Meta:
        model = tweet
        fields = ['text', 'photo']

class UserRegistration(UserCreationForm):
    email = forms.EmailField()    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2') #Using Built in table modules

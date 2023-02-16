from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Show
from django.contrib.auth.models import User


class ShowForm(forms.ModelForm):
    class Meta:
        model = Show
        fields = '__all__'


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        

class LoginUserForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from . import models


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = models.User
        fields = ['name', 'username', 'email', 'password1', 'password2']


class UserForm(ModelForm):
    class Meta:
        model = models.User
        fields = ['avatar','name','username', 'email','bio']
from django.forms import ModelForm
# imports django user creation form 
from django.contrib.auth.forms import UserCreationForm
from django import forms
# imports the default User model 
from django.contrib.auth.models import User


# the usage of this form is to create extra field like email 
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
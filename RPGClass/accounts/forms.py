from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UpdateForm(forms.Form):
    user_name = forms.CharField(label='username', max_length=100)
    password = forms.CharField(label='password', max_length=100)
    nickname = forms.CharField(label='Nickname', max_length=100)

    def validate(self, username, password):
        if (not authenticate(username=username, password=password)):
            self.add_error('password', "credentials do not match!")
            return False
        return True

class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2',)


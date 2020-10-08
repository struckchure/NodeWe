from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from . import models


class SignUpForm(UserCreationForm):
    class Meta:
        model = models.User
        fields = [
            'username',
            'email',
        ]


# class SignInForm(AuthenticationForm):
#     pass

class SignInForm(forms.Form):
	username = forms.CharField(max_length=50, required=True)
	password = forms.CharField(
		max_length=100,
		required=True,
		widget=forms.PasswordInput
	)

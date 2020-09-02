from django import forms

from . import models


class SignInForm(forms.Form):
	username = forms.CharField(max_length=50, required=True)
	password = forms.CharField(max_length=100, required=True)

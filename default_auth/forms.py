"""
Forms for authorization and registration.
"""
import re

from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class SignupForm(ModelForm):
    """
    Form for registering a new user.
    """
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Re-Password'}))

    class Meta:
        """
        Form model with fields.
        """
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def clean_username(self):
        """
        Check if the username already exists in the database.
        """
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists.")
        return username

    def clean_password(self):
        """
        Validate the password strength.
        """
        password = self.cleaned_data.get('password')
        if not self.is_valid_password(password):
            raise ValidationError("Password is too weak.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password and password2 and password != password2:
            self.add_error('password2', "Passwords don't match")

    def is_valid_password(self, password):
        """
        Check if the password is strong.
        """
        if len(password) < 8:
            return False
        if not re.search(r'[A-Z]', password):
            return False
        if not re.search(r'[a-z]', password):
            return False
        if not re.search(r'[0-9]', password):
            return False
        return True


class LoginForm(forms.Form):
    """
    Authorization form.
    """
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, UsernameField, \
    PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
    )
    password2 = forms.CharField(
        label=_("Password Confirmation"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password Confirmation'}),
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'pattern': '^[a-zA-Z]+',
                'required': 'required',
                'title': 'Only letters are allowed.',
                'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'pattern': '^[a-zA-Z]+',
                'required': 'required',
                'title': 'Only letters are allowed.',
                'placeholder': 'Last Name'
            })
        }
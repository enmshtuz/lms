from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import Profile, User
from django import forms

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

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email


class ResendVerificationEmailForm(forms.Form):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your email'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is not associated with any user.")
        return email


class LoginForm(AuthenticationForm):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"autofocus": True, "class": "form-control", "placeholder": "Email"}),
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the username field
        self.fields.pop('username', None)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        if not email or not password:
            raise forms.ValidationError("Email and password are required.")
        return cleaned_data


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'date_of_birth', 'avatar']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set first name and last name fields as required
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['date_of_birth'].required = False


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()

class UserSetPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
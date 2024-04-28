from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import View
from django.views.generic.edit import FormView
from .forms import RegistrationForm, ResendVerificationEmailForm, LoginForm, ProfileForm, ForgotPasswordForm, \
    UserSetPasswordForm
from .models import EmailVerification, Profile, SiteSettings, User, PasswordReset
import uuid

UserModel = get_user_model()


def register(request):
    site_settings = SiteSettings.objects.first()
    if site_settings.open_registration:
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = form.save()
                user.set_password(form.cleaned_data['password1'])
                user.save()

                token = generate_verification_token()
                verification = EmailVerification.objects.create(user=user, token=token)
                verification.save()
                uid = urlsafe_base64_encode(force_bytes(user.pk))

                send_verification_email(user, token, uid)

                return redirect('register_success')
        else:
            form = RegistrationForm()
        return render(request, 'register.html', {'form': form})
    else:
        return redirect('register_closed')


def register_closed(request):
    return render(request, 'register_closed.html')


def register_success(request):
    return render(request, 'register_success.html')


def generate_verification_token():
    return uuid.uuid4()


def send_verification_email(user, token, uid):
    verification_link = f'http://localhost:8000/account/verify/{uid}/{token}/'
    subject = 'Verify Your Email Address'
    message = f'Hi {user.first_name},\nPlease click on the link below to verify your email address:\n{verification_link}'
    user_email = user.email
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user_email])


def invalid_link(request):
    return render(request, 'invalid_link.html')


def verify_email(request, token, uid):
    verification = EmailVerification.objects.filter(token=token).first()
    if verification:
        if timezone.now() - verification.created_at <= timezone.timedelta(hours=5):
            verification.user.is_active = True
            verification.user.save()
            verification.token = None
            verification.created_at = None
            verification.save()
            return redirect('login')
        else:
            return redirect('verification_failure')
    return redirect('invalid_link')


def verification_failure(request):
    if request.method == 'POST':
        form = ResendVerificationEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                verification = get_object_or_404(EmailVerification, user=user)
                verification.token = generate_verification_token()
                verification.created_at = timezone.now()
                verification.save()
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                send_verification_email(user, verification.token, uid)
                return redirect('register_success')
    else:
        form = ResendVerificationEmailForm()
    return render(request, 'verification_failure.html', {'form': form})


def authenticate(request, email=None, password=None):
    if email is None or password is None:
        return None

    try:
        user = UserModel.objects.get(email=email)
    except UserModel.DoesNotExist:
        return None

    if check_password(password, user.password):
        return user
    else:
        return None


class UserLoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('profile')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('profile')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(request=self.request, email=email, password=password)
        if user is not None:
            if hasattr(user, 'profile'):
                profile = user.profile
            else:
                profile = Profile(user=user)
                profile.save()

            verification = EmailVerification.objects.filter(user=user).first()
            if verification and verification.token is None:
                login(self.request, user)
                return super().form_valid(form)
            else:
                form.add_error(None, 'Your email is not verified.')
        else:
            form.add_error(None, 'Invalid email or password.')
        return self.form_invalid(form)


class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        return redirect(reverse_lazy('login'))


@login_required
def profile(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    return render(request, 'profile.html', {'profile': profile})


@login_required
def edit_profile(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            if 'avatar' in request.FILES:
                profile.avatar = request.FILES['avatar']
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form})


@login_required
@staff_member_required
def site_settings(request):
    site_settings_instance, _ = SiteSettings.objects.get_or_create(pk=1)

    if request.method == 'POST':
        site_settings_instance.open_registration = bool(request.POST.get('open_registration'))
        site_settings_instance.invitation_link_expiration = timezone.timedelta(
            days=int(request.POST.get('invitation_link_expiration_days')))
        site_settings_instance.verification_link_expiration = timezone.timedelta(
            hours=int(request.POST.get('verification_link_expiration_hours')))
        site_settings_instance.save()

        messages.success(request, 'Settings saved successfully.')
        return HttpResponseRedirect(reverse('profile'))

    return render(request, 'site_settings.html', {'site_settings': site_settings_instance})


@login_required
@staff_member_required
def send_invitation_email(request):
    site_settings_instance, _ = SiteSettings.objects.get_or_create(pk=1)

    if request.method == 'POST':
        site_settings_instance.open_registration = bool(request.POST.get('open_registration'))
        site_settings_instance.invitation_link_expiration = timezone.timedelta(
            days=int(request.POST.get('invitation_link_expiration_days')))
        site_settings_instance.verification_link_expiration = timezone.timedelta(
            hours=int(request.POST.get('verification_link_expiration_hours')))
        site_settings_instance.save()

        messages.success(request, 'Settings saved successfully.')
        return HttpResponseRedirect(reverse('profile'))

    return render(request, 'send_invitation_link.html', {'site_settings': site_settings_instance})


def generate_reset_token():
    return uuid.uuid4().hex  # Return a hexadecimal representation of the UUID


def password_reset(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()
            if user:

                verification = EmailVerification.objects.filter(user=user).first()

                if verification.token is None:
                    form.add_error(None, 'Invalid email or password.')

                token = generate_reset_token()
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset, _ = PasswordReset.objects.get_or_create(
                    user=user,
                )
                reset.token = token
                reset.created_at = timezone.now()
                reset.save()
                send_reset_email(user, token, uid)
                return redirect('password_reset_complete')
    else:
        form = ForgotPasswordForm()
    return render(request, 'password_reset.html', {'form': form})


def password_reset_complete(request):
    return render(request, 'password_reset_complete.html')


def send_reset_email(user, token, uid):
    reset_link = f'http://localhost:8000/account/password_reset/{uid}/{token}/'  # Change the URL as per your project's URL structure
    subject = 'Reset Your Password'  # Change the subject if needed
    message = f'Hi {user.first_name},\nPlease click on the link below to reset your password:\n{reset_link}'
    user_email = user.email
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user_email])


def reset_password(request, token, uid):
    if request.method == 'POST':
        form = UserSetPasswordForm(request.POST)
        if form.is_valid():
            reset = PasswordReset.objects.filter(token=token).first()
            if reset:
                if timezone.now() - reset.created_at <= timezone.timedelta(hours=5):
                    password = form.cleaned_data['password']
                    reset.user.set_password(password)
                    reset.user.save()
                    reset.token = None
                    reset.created_at = None
                    reset.save()
                    return redirect('login')
                else:
                    return redirect('invalid_link')
            return redirect('invalid_link')
    else:
        form = UserSetPasswordForm()
    return render(request, 'password_reset_confirm.html', {'form': form})

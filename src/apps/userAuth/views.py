from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import View
from django.views.generic.edit import FormView
from .forms import RegistrationForm, ResendVerificationEmailForm, LoginForm, ProfileForm, ForgotPasswordForm, \
    UserSetPasswordForm, InvitationEmailForm, ClosedRegistrationForm
from .models import EmailVerification, Profile, SiteSettings, User, PasswordReset, InvitationLink, UserRoles
import os
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

                UserRoles.objects.create(user=user, role='user')

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


def closed_register(request, uid, token):
    site_settings = SiteSettings.objects.first()

    if not site_settings.open_registration:
        link_expiration = site_settings.invitation_link_expiration_days

        try:
            invitation_link = InvitationLink.objects.get(token=token)
        except InvitationLink.DoesNotExist:
            return render(request, 'invalid_link.html')

        if timezone.now() - invitation_link.created_at > timezone.timedelta(days=link_expiration):
            return render(request, 'invalid_link.html')

        invitation_link.status = 'success'
        invitation_link.save()

        if request.method == 'POST':
            form = ClosedRegistrationForm(request.POST)
            if form.is_valid():
                user = form.save()
                user.set_password(form.cleaned_data['password1'])
                user.save()

                UserRoles.objects.create(user=user, role='user')

                verify_token = generate_verification_token()
                verification = EmailVerification.objects.create(user=user, token=verify_token)
                verification.save()
                verify_uid = urlsafe_base64_encode(force_bytes(user.pk))

                send_verification_email(user, verify_token, verify_uid)

                return redirect('register_success')
        else:
            form = ClosedRegistrationForm()
        return render(request, 'closed_register.html', {'form': form, 'uid': uid, 'token': token})
    else:
        return redirect('register')


def register_closed(request):
    return render(request, 'register_closed.html')


def register_success(request):
    return render(request, 'register_success.html')


def update_expired_links_status():
    site_settings = SiteSettings.objects.first()
    link_expiration = site_settings.invitation_link_expiration_days
    expired_links = InvitationLink.objects.filter(
        created_at__lte=timezone.now() - timezone.timedelta(days=link_expiration),
        status='pending'
    )
    for link in expired_links:
        link.status = 'expired'
        link.save()


def register_invitation(request):
    if is_admin(request):
        update_expired_links_status()
        invitation_links = InvitationLink.objects.all()
        return render(request, 'registration_invitation.html', {'invitation_links': invitation_links})
    else:
        return render(request, 'unauthorized_access.html')


def send_invitation_email(email, token, uid):
    link = f'http://localhost:8000/account/register_invitation/{uid}/{token}/'
    subject = 'Invitation of Registration'
    message = f'Hi,\nPlease click on the link below to register:\n{link}'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])


@login_required
@staff_member_required
def register_invite(request):
    update_expired_links_status()
    invitation_links = InvitationLink.objects.all()
    if request.method == 'POST':
        form = InvitationEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            token = generate_token()
            uid = urlsafe_base64_encode(force_bytes(email))
            invitation_link = InvitationLink.objects.create(
                email=email,
                link=f'http://localhost:8000/account/register_invitation/{uid}/{token}/',
                token=token,
                status='pending'
            )
            send_invitation_email(email, invitation_link.token, uid)
            return redirect('register_invite')
    else:
        form = InvitationEmailForm()
    return render(request, 'registration_invitation.html', {'form': form, 'invitation_links': invitation_links})


@login_required
@staff_member_required
def delete_invitation_link(request, pk):
    invitation_link = get_object_or_404(InvitationLink, pk=pk)
    if request.method == 'POST':
        invitation_link.delete()
        # Redirect to register_invitation after deleting the object
        return redirect('register_invitation')
    invitation_links = InvitationLink.objects.all()
    return render(request, 'registration_invitation.html', {'invitation_links': invitation_links})


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
        site_settings = SiteSettings.objects.first()
        link_expiration = site_settings.verification_link_expiration_hours
        if timezone.now() - verification.created_at <= timezone.timedelta(hours=link_expiration):
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
                next_url = self.request.GET.get('next')
                if next_url:
                    self.success_url = next_url
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
def serve_avatar(request, filename):
    avatar_path = os.path.join(settings.AVATAR_UPLOAD_DIR, filename)
    try:
        with open(avatar_path, "rb") as f:
            return HttpResponse(f.read(), content_type="image/png")
    except FileNotFoundError:
        return HttpResponse("Avatar not found", status=404)


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
            if 'avatar' in request.FILES and 'delete_avatar' in request.POST:
                form.add_error(None, "Either upload a new avatar or delete the existing one, not both.")
                return render(request, 'edit_profile.html', {'form': form})

            if 'avatar' in request.FILES:
                profile.avatar = request.FILES['avatar']
                profile.save()  # Save the profile to get the file path
                # Get the file path of the saved avatar
                avatar_path = profile.avatar.path
                # Set permissions for the file
                os.chmod(avatar_path, 0o644)  # Adjust permissions as needed
            if 'delete_avatar' in request.POST:
                profile.avatar.delete()

            # Update user authentication data
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()

            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form})


@login_required
def site_settings(request):
    if is_admin(request):
        site_settings_instance, _ = SiteSettings.objects.get_or_create(pk=1)

        if request.method == 'POST':
            site_settings_instance.open_registration = bool(request.POST.get('open_registration'))
            site_settings_instance.verification_link_expiration_hours = int(
                request.POST.get('verification_link_expiration_hours'))
            site_settings_instance.invitation_link_expiration_days = int(
                request.POST.get('invitation_link_expiration_days'))
            site_settings_instance.save()

            messages.success(request, 'Settings saved successfully.')
            return HttpResponseRedirect(reverse('profile'))

        return render(request, 'site_settings.html', {'site_settings': site_settings_instance})
    else:
        return render(request, 'unauthorized_access.html')


def generate_token():
    return uuid.uuid4().hex


def send_reset_email(user, token, uid):
    reset_link = f'http://localhost:8000/account/password_reset/{uid}/{token}/'
    subject = 'Reset Your Password'
    message = f'Hi {user.first_name},\nPlease click on the link below to reset your password:\n{reset_link}'
    user_email = user.email
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user_email])


def password_reset(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()

            token = generate_token()
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


def reset_password(request, token, uid):
    reset = PasswordReset.objects.filter(token=token).first()
    site_settings = SiteSettings.objects.first()
    link_expiration = site_settings.verification_link_expiration_hours
    if reset and reset.token is not None:
        if timezone.now() - reset.created_at > timezone.timedelta(hours=link_expiration):
            return render(request, 'invalid_link.html')

    if request.method == 'POST':
        form = UserSetPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            reset.user.set_password(password)
            reset.user.save()
            reset.token = None
            reset.created_at = None
            reset.save()
            return redirect('login')
    else:
        form = UserSetPasswordForm()
    return render(request, 'password_reset_confirm.html', {'form': form})


@login_required
def manage_roles(request):
    if is_admin(request):
        users = User.objects.all()
        if request.method == 'POST':
            for user in users:
                new_role = request.POST.get(f"roleSelect{user.id}")
                user_roles = UserRoles.objects.get_or_create(user=user)[0]
                if user_roles.role != new_role:
                    user_roles.role = new_role
                    user_roles.save()
                    user.groups.clear()
                    if new_role == 'admin':
                        user.is_staff = True
                        user.is_superuser = True
                    elif new_role == 'manager':
                        user.is_staff = True
                        user.is_superuser = False
                    else:
                        user.is_staff = False
                        user.is_superuser = False
                    user.save()
        users = User.objects.all()
        return render(request, 'manage_roles.html', {'users': users})
    else:
        return render(request, 'unauthorized_access.html')


def is_admin(request):
    user = request.user
    if user.is_authenticated:
        try:
            user_role = UserRoles.objects.get(user=user)
            return user_role.role == 'admin'
        except UserRoles.DoesNotExist:
            return False
    return False

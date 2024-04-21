from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .forms import RegistrationForm, ResendVerificationEmailForm
from .models import EmailVerification
import uuid

def register(request):
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
    return redirect('verification_failure')


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

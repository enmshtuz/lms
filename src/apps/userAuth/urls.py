from django.urls import path
from .views import (register, register_success, register_closed, verify_email,
                    verification_failure, invalid_link,
                    UserLoginView, LogoutView, reset_password,
                    password_reset, password_reset_complete,
                    profile, edit_profile, site_settings, send_invitation_email)

urlpatterns = [
    path('register/', register, name='register'),
    path('register_closed/', register_closed, name='register_closed'),
    path('register/success', register_success, name='register_success'),
    path('register/failure', verification_failure, name='verification_failure'),
    path('register/invalid_link', invalid_link, name='invalid_link'),
    path('verify/<uid>/<token>/', verify_email),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('password_reset/', password_reset, name='password_reset'),
    path('password_reset_complete/', password_reset_complete, name='password_reset_complete'),
    path('password_reset/<uid>/<token>/', reset_password, name='reset_password'),





    path('profile/', profile, name='profile'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('site_settings/', site_settings, name='site_settings'),
    path('send_invitation_email/', send_invitation_email, name='send_invitation_email'),
]

from django.urls import path
from .views import (register, register_closed, register_invitation,
                    register_invite, closed_register, delete_invitation_link,
                    register_success, verification_failure, invalid_link,
                    verify_email, UserLoginView, LogoutView, password_reset,
                    password_reset_complete, reset_password,
                    serve_avatar, profile, edit_profile, site_settings,
                    manage_roles)

urlpatterns = [
    path('register/', register, name='register'),
    path('register_closed/', register_closed, name='register_closed'),
    path('register/invitation/', register_invitation, name='register_invitation'),
    path('register/invite/', register_invite, name='register_invite'),
    path('register_invitation/<uid>/<token>/', closed_register, name='closed_register'),
    path('register/invite/delete/<int:pk>/', delete_invitation_link, name='delete_invitation_link'),
    path('register/success', register_success, name='register_success'),
    path('register/failure', verification_failure, name='verification_failure'),
    path('register/invalid_link', invalid_link, name='invalid_link'),
    path('verify/<uid>/<token>/', verify_email),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password_reset/', password_reset, name='password_reset'),
    path('password_reset_complete/', password_reset_complete, name='password_reset_complete'),
    path('password_reset/<uid>/<token>/', reset_password, name='reset_password'),
    path('avatars/<str:filename>/', serve_avatar, name='serve_avatar'),
    path('profile/', profile, name='profile'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('site_settings/', site_settings, name='site_settings'),
    path('manage_roles/', manage_roles, name='manage_roles'),
]

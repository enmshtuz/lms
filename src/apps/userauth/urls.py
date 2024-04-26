from django.urls import path
from .views import (register, register_success, register_closed, verify_email, verification_failure,
                    UserLoginView, LogoutView,
                    ForgotPasswordView, PasswordResetConfirmView, #PasswordResetCompleteView,
                    profile, edit_profile, site_settings)

urlpatterns = [
    path('register/', register, name='register'),
    path('register_closed/', register_closed, name='register_closed'),
    path('register/success', register_success, name='register_success'),
    path('register/failure', verification_failure, name='verification_failure'),
    path('verify/<uid>/<token>/', verify_email),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('password_reset/', ForgotPasswordView.as_view(), name='password_reset'),
    path('password_reset_confirm/<uid>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    #path('password_reset_complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),



    path('profile/', profile, name='profile'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('site_settings/', site_settings, name='site_settings'),
]

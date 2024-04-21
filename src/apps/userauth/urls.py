from django.urls import path
from .views import register, register_success, verify_email, verification_failure

urlpatterns = [
    path('register/', register, name='register'),
    path('register/success', register_success, name='register_success'),
    path('register/failure', verification_failure, name='verification_failure'),
    path('verify/<uid>/<token>/', verify_email),
]

from django.urls import path
from .views import register, register_success

urlpatterns = [
    path('register/', register, name='register'),
    path('register/success', register_success, name='register_success'),
]

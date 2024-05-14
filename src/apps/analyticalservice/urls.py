from django.urls import path
from . import views

urlpatterns = [
    path('', views.reports, name='reports'),
    path('logout/', views.logoutUser, name='logout'),
]
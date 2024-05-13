from django.urls import path
from . import views


urlpatterns = [
    # path('submit_feedback/<int:course_id>/', views.submit_feedback, name='submit_feedback'),
    path('feedback/submit_feedback/<int:course_id>/', views.submit_feedback, name='submit_feedback'),


]

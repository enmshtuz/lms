from django.urls import path
from . import views

urlpatterns = [

    path('badge/create/', views.create_badge, name='create_badge'),
    path('badge/<int:badge_id>/update/', views.update_badge, name='update_badge'),
    path('badge/<int:badge_id>/delete/', views.badge_delete, name='delete_badge'),
    path('badges/', views.badge_list, name='badge_list'),
    # path('course/create/', views.create_course, name=' create_course'),
    # path('course/<int:course_id>/update/', views.update_course, name='update_course'),

]

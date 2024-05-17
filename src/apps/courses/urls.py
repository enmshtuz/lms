from django.urls import path
from . import views


urlpatterns = [
    path('create/', views.course_create, name='course_create'),
    path('<int:pk>/update/', views.course_update, name='course_update'),
    path('<int:pk>/delete/', views.course_delete, name='course_delete'),
    path('', views.course_list, name='course_list'),
    path('<int:pk>/publish/', views.publish_course, name='publish_course'),
    path('<int:pk>/unpublish/', views.unpublish_course, name='unpublish_course'),
    path('<int:pk>/unenroll/', views.unenroll_course, name='unenroll_course'),
    path('<int:pk>/enroll/', views.enroll_course, name='enroll_course'),
    path('<int:pk>/details/', views.details_course_page, name='details_course'),
    path('<int:pk>/details/update_progress/', views.update_progress, name='update_progress'),
    path('<int:pk>/details/users_list/', views.enroll_user_list, name='users_list'),
    path('<int:pk>/details/force_enroll/', views.force_enroll, name='force_enroll'),
    path('my-courses/', views.my_courses_list, name='my_courses_list'),
]
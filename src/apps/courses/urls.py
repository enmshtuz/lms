from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index)
    # path('create/', views.create_course, name='create_course'),
    # path('update/<int:course_id>/', views.update_course, name='update_course'),
    #
    path('create/', views.course_create, name='course_create'),
    path('<int:pk>/update/', views.course_update, name='course_update'),
    path('<int:pk>/delete/', views.course_delete, name='course_delete'),
    # path('<int:pk>/publish/', views.publish_course, name='publish_course'),
    path('published/', views.published_course_list, name='published_course_list'),
    # path('<int:pk>/unenroll/', views.unenroll_course, name='unenroll_course'),
    # path('<int:pk>/enroll/', views.unenroll_course, name='enroll_course'),
    path('', views.course_list, name='course_list'),
    path('<int:course_id>/enroll/', views.enroll_course, name='enroll_course'),
    path('<int:course_id>/unenroll/', views.unenroll_course, name='unenroll_course'),
    path('<int:pk>/publish/', views.publish_course, name='publish_course'),
    path('<int:pk>/unpublish/', views.unpublish_course, name='unpublish_course'),
    path('<int:pk>/details/', views.course_details, name='course_details'),


]
from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index),
    path('create/', views.create_quiz, name='create_quiz'),
    path('update/<int:quiz_id>/', views.update_quiz, name='update_quiz'),
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('quiz/', views.quiz_list, name='quiz_list'),
    path('quiz/<int:quiz_id>/delete/', views.quiz_delete, name='quiz_delete'),
    # path('add_question/<int:quiz_id>/', views.add_question, name='add_question'),
    # path('add_answer/<int:quiz_id>/<int:question_id>/', views.add_answer, name='add_answer'),
]
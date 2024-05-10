from django.urls import path
from . import views

urlpatterns = [
    #path('', views.index),
    path('create/', views.quiz_create, name='quiz_create'),
    path('', views.quiz_list, name="quiz_list"),
    path('<int:pk>/delete/', views.quiz_delete, name='quiz_delete'),
    path('<int:pk>/update/', views.quiz_update, name='quiz_update'),
    path('published/', views.published_quiz_list, name='published_quiz_list'),
    path('<int:pk>/publish/', views.publish_quiz, name='publish_quiz'),
    path('<int:pk>/unpublish/', views.unpublish_quiz, name='unpublish_quiz'),
    path('create_question_and_answer/', views.create_question_and_answer, name='create_question_and_answer'),
    # path('create-question/', views.create_question, name='create_question'),
    # path('quiz/create-answer/<int:question_id>/', views.create_answer, name='create_answer'),
    # path('take-quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
]
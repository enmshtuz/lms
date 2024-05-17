from django.urls import path
from . import views

urlpatterns = [
    path('', views.news_list, name='news_list'),
    path('subscribe/', views.subscribe, name='subscribe'),
    # path('submit/', views.submit, name='submit'),
    path('create/', views.create_news, name='create_news'),
    path('publish/<int:news_id>/', views.publish_news, name='publish_news'),
]

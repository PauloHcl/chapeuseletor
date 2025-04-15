from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('quiz/', views.quiz, name='quiz'),
    path('choose-house/', views.choose_house, name='choose_house'),
    path('result/', views.result, name='result'),
]

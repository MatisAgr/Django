from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/active/', views.task_active, name='task_active'),
    path('tasks/<int:pk>/', views.task_detail, name='task_detail'), #detail en fonction de l'id
]

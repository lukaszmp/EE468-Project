from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
	path('admin/', views.admin, name='admin'),
	path('professor/', views.professor, name='professor'),
	path('student/', views.student, name='student'),
	path('', views.user_login, name='login'),
]
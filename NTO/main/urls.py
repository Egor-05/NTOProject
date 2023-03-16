from django.contrib import admin
from django.urls import path
import main.views as views


urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('result/', views.respage, name='marko'),
    path('', views.main, name='homepage'),
]


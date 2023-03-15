from django.contrib import admin
from django.urls import path
import main.views as views
from django.views.generic import TemplateView


urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    
    path('', TemplateView.as_view(template_name="base.html"), name='homepage'),
]


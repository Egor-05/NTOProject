from django.views.generic import CreateView, UpdateView, TemplateView
import django.contrib.auth.views as AuthViews
from django.urls.base import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.auth.models import User

from .forms import RegisterUserForm, LoginUserForm
# Create your views here.


class RegisterView(CreateView):
    form_class = RegisterUserForm
    template_name = 'base_form.html'
    extra_context = {
        'page_title': 'Регистрация',
        'button_text': 'Создать аккаунт',
        'form_title': 'Регистрация',
    }
    success_url = reverse_lazy('main:homepage')
    success_message = (
        'Вы <strong>успешно</strong> зарегистрировались'
    )

    def form_valid(self, form):
        result = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        messages.add_message(
            self.request, messages.SUCCESS, self.success_message,
            extra_tags='alert-success'
            )
        return result


class LoginView(AuthViews.LoginView):
    form_class = LoginUserForm
    template_name = 'base_form.html'
    extra_context = {
        'page_title': 'Вход',
        'button_text': 'Войти',
        'form_title': 'Вход в аккаунт',
    }
    

class LogoutView(LoginRequiredMixin, AuthViews.LogoutView):
    template_name = 'users/logout.html'


class MainPage(TemplateView):
    template_name = 'base.html'

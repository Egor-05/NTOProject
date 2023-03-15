from django.views.generic import CreateView, FormView, TemplateView
import django.contrib.auth.views as AuthViews
from django.urls.base import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import render, redirect

from .forms import RegisterUserForm, LoginUserForm, ShareParamsForm


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


# class MainPage(FormView):
#     template_name = 'base_form.html'
#     form_class = ShareParamsForm

#     def form_valid(self, form):
#         a = form.cleaned_data["share_names"]
#         print(a)
#         self.params = [a, form.cleaned_data["minimum_profit"], form.cleaned_data["maximum_risk"]]
#         return super().form_valid(form)

#     def get_success_url(self):
#         return reverse('main:marko', kwargs={'params': self.params})


class ResultPage(TemplateView):
    template_name = 'base.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response({})


def main(request):
    if request.method == 'POST':
        form = ShareParamsForm(request.POST)
        if form.is_valid():
            params = [form.cleaned_data["share_names"], form.cleaned_data["minimum_profit"],
                      form.cleaned_data["maximum_risk"]]
            print(params)
            return redirect('/result', kwargs={'params': params})

    else:
        form = ShareParamsForm()
    return render(request, 'base_form.html', {'form': form})
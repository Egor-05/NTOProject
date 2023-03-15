import django.contrib.auth.forms as UserForms
from django.contrib.auth.models import User
from django import forms


class FormStyleMixin(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            attrs = field.field.widget.attrs
            if 'class' not in attrs:
                attrs['class'] = 'form-control'
            else:
                attrs['class'] += ' form-control'


class RegisterUserForm(UserForms.UserCreationForm, FormStyleMixin):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class LoginUserForm(UserForms.AuthenticationForm, FormStyleMixin):
    username = forms.CharField(label='Логин', max_length=150)


class ShareParams(forms.Form):
    share_names = forms.MultipleChoiceField(choices=[1, 2, 3], label='Выберите интересующие вас акции')
    minimum_profit = forms.FloatField(min_value=0)

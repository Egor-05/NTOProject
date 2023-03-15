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


class ShareParamsForm(forms.Form):
    share_names = forms.MultipleChoiceField(label='Названия акций',
                                            choices=[('1', '1'), ('1', '1'), ('1', '1'), ('1', '1'), ('2', '2'),
                                                     ('3цукацууаца', 'ауаываываыа3')],
                                            widget=forms.CheckboxSelectMultiple)
    minimum_profit = forms.FloatField(min_value=0, required=False, label='Минимальня выгода')
    maximum_risk = forms.FloatField(min_value=0, max_value=100, required=False, label='Максимальный риск')

    def clean_share_names(self):
        if len(self.cleaned_data['share_names']) > 5:
            raise forms.ValidationError('Можно выбрать не более 5-ти полей')
        return self.cleaned_data['share_names']

    def clean_maximum_risk(self):
        minimum_profit = self.cleaned_data.get('minimum_profit')
        maximum_risk = self.cleaned_data.get('maximum_risk')
        if not minimum_profit and not maximum_risk:
            raise forms.ValidationError('Заполните или поле минимальная выгода или поле максимальный риск')
        if minimum_profit and maximum_risk:
            raise forms.ValidationError('Заполните или поле минимальная выгода или поле максимальный риск')
        return self.cleaned_data['maximum_risk']
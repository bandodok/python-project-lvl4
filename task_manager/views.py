from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic.edit import FormView
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils.translation import ugettext as _


def index(request):
    return render(request, 'index.html')


class LoginForm(forms.Form):
    username = forms.CharField(label=_('Username'))
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password')


class Login(FormView):

    form_class = LoginForm
    template_name = 'users/login_user.html'

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            messages.success(self.request, 'Вы залогинены')
            login(request, user)
            return redirect('/')
        else:
            messages.error(self.request, 'Пожалуйста, введите правильные имя пользователя и пароль. Оба поля могут быть чувствительны к регистру.')
            return redirect(self.request.META.get('HTTP_REFERER'))


class Logout(FormView):

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.success(self.request, 'Вы разлогинены')
        return redirect(request.META.get('HTTP_REFERER'))

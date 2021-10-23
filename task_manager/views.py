from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse


def index(request):
    return render(request, 'index.html')


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password')


class Login(FormView):

    form_class = LoginForm
    template_name = 'login_user.html'

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('users')
        else:
            return HttpResponse('invalid')


class Logout(FormView):

    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('users')

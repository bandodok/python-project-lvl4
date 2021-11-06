from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView, FormView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


# Create your views here.
class Index(ListView):
    model = User
    paginate_by = 100
    template_name = 'users/user_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class MyRegisterFormView(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')


class Create(FormView):
    form_class = MyRegisterFormView
    success_url = '/login/'
    template_name = 'users/create_user.html'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Пользователь успешно зарегистрирован')
        return super(Create, self).form_valid(form)

    def form_invalid(self, form):
        return super(Create, self).form_invalid(form)


class Update(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    model = User
    template_name = 'users/update_user.html'
    success_url = '/users/'
    permission_denied_message = 'Permission denied'
    form_class = MyRegisterFormView

    def test_func(self):
        obj = self.get_object()
        return obj.id == self.request.user.id

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return redirect('/users/')

    def form_invalid(self, form):
        messages.error(self.request, 'Поля заполнены неверно')
        return super(Update, self).form_invalid(form)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Пользователь успешно изменен')
        return super(Update, self).form_valid(form)


class Delete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'users/delete_user.html'
    success_url = '/users/'
    permission_denied_message = 'Permission denied'

    def test_func(self):
        obj = self.get_object()
        return obj.id == self.request.user.id

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return redirect('/users/')

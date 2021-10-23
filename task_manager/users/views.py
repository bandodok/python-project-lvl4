from django.utils import timezone
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView, FormView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
class Index(ListView):
    model = User
    paginate_by = 100
    template_name = 'user_list.html'

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
    success_url = '/users/'
    template_name = 'create_user.html'

    def form_valid(self, form):
        form.save()
        return super(Create, self).form_valid(form)

    def form_invalid(self, form):
        return super(Create, self).form_invalid(form)


class Update(UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'password']
    template_name = 'update_user.html'
    success_url = '/users/'


class Delete(DeleteView):
    model = User
    template_name = 'delete_user.html'
    success_url = '/users/'

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import DetailView
from django.views.generic.edit import FormView, UpdateView, DeleteView
from django_filters.views import FilterView
from task_manager.tasks.models import Task
from task_manager.labels.models import Label
from django import forms
import django_filters
from django.utils.translation import ugettext as _


class TaskView(DetailView):
    template_name = 'tasks/task.html'
    queryset = Task.objects.all()


class TaskCreationForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'label']


class TaskFilter(django_filters.FilterSet):
    try:
        label = django_filters.ModelChoiceFilter(
            label=_('label'),
            queryset=Label.objects.all()
        )
    except Exception:
        pass

    class Meta:
        model = Task
        fields = ['status', 'executor', 'label']


class Index(LoginRequiredMixin, FilterView):
    model = Task
    paginate_by = 100
    template_name = 'tasks/task_list.html'
    filterset_class = TaskFilter

    def get_queryset(self):
        if self.request.GET.get('self_tasks') == 'on':
            user = self.request.user
            return Task.objects.filter(author=user)
        return Task.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        return context

    def handle_no_permission(self):
        messages.error(self.request, 'Permission denied')
        return redirect('/')


class Create(LoginRequiredMixin, FormView):
    model = Task
    template_name = 'tasks/create_task.html'
    success_url = '/tasks/'
    form_class = TaskCreationForm

    def form_valid(self, form):
        task = form.save(commit=False)
        task.author = self.request.user
        task.save()
        if form.cleaned_data['label']:
            for label in form.cleaned_data['label']:
                task.label.add(label)
            task.save()
        messages.success(self.request, 'Задача успешно создана')
        return super(Create, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Task not created')
        return super(Create, self).form_invalid(form)

    def handle_no_permission(self):
        messages.error(self.request, 'Permission denied')
        return redirect('/')


class Update(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'tasks/update_task.html'
    success_url = '/tasks/'
    fields = ['name', 'description', 'status', 'executor', 'label']

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Задача успешно изменена')
        return super(Update, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Task not changed')
        return super(Update, self).form_invalid(form)

    def handle_no_permission(self):
        messages.error(self.request, 'Permission denied')
        return redirect('/')


class Delete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete_task.html'
    success_url = '/tasks/'

    def test_func(self):
        task = self.get_object()
        return task.author.id == self.request.user.id

    def handle_no_permission(self):
        messages.error(self.request, 'Permission denied')
        return redirect('/tasks')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Задача успешно удалена')
        return super(Delete, self).delete(request)

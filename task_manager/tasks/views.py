from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import DetailView
from django.views.generic.edit import FormView, UpdateView, DeleteView
from django.views.generic.list import ListView
from task_manager.tasks.models import Task
from django import forms


class TaskView(DetailView):
    template_name = 'tasks/task.html'
    queryset = Task.objects.all()


class TaskCreationForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']


class Index(LoginRequiredMixin, ListView):
    model = Task
    paginate_by = 100
    template_name = 'tasks/task_list.html'

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
        for label in form.cleaned_data['labels']:
            task.labels.add(label)
        task.save()
        messages.success(self.request, 'Task created')
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
    fields = ['name', 'description', 'status', 'executor', 'labels']

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Task changed')
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

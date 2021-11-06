from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView, UpdateView, DeleteView
from django.views.generic.list import ListView
from task_manager.statuses.models import Status
from django import forms


class StatusCreationForm(forms.ModelForm):

    class Meta:
        model = Status
        fields = ['name']


class Index(LoginRequiredMixin, ListView):
    model = Status
    paginate_by = 100
    template_name = 'statuses/status_list.html'

    def handle_no_permission(self):
        messages.error(self.request, 'Permission denied')
        return redirect('/')


class Create(LoginRequiredMixin, FormView):
    model = Status
    template_name = 'statuses/create_status.html'
    success_url = '/statuses/'
    form_class = StatusCreationForm

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Status created')
        return super(Create, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Status not created')
        return super(Create, self).form_invalid(form)

    def handle_no_permission(self):
        messages.error(self.request, 'Permission denied')
        return redirect('/')


class Update(LoginRequiredMixin, UpdateView):
    model = Status
    template_name = 'statuses/update_status.html'
    success_url = '/statuses/'
    fields = ['name']

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Status changed')
        return super(Update, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Status not changed')
        return super(Update, self).form_invalid(form)

    def handle_no_permission(self):
        messages.error(self.request, 'Permission denied')
        return redirect('/')


class Delete(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'statuses/delete_status.html'
    success_url = '/statuses/'

    def handle_no_permission(self):
        messages.error(self.request, 'Permission denied')
        return redirect('/')

    def delete(self, request, *args, **kwargs):
        status = self.get_object()
        if status.status.all():
            messages.error(self.request, "Невозможно удалить статус, потому что он используется")
            return redirect(reverse_lazy('statuses'))
        messages.success(self.request, 'Статус успешно удалён')
        return super(Delete, self).delete(request)

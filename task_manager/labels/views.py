from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic.edit import FormView, UpdateView, DeleteView
from django.views.generic.list import ListView
from task_manager.labels.models import Label
from django import forms


class LabelCreationForm(forms.ModelForm):

    class Meta:
        model = Label
        fields = ['name']


class Index(LoginRequiredMixin, ListView):
    model = Label
    paginate_by = 100
    template_name = 'labels/label_list.html'

    def handle_no_permission(self):
        messages.error(self.request, 'Permission denied')
        return redirect('/')


class Create(LoginRequiredMixin, FormView):
    model = Label
    template_name = 'labels/create_label.html'
    success_url = '/labels/'
    form_class = LabelCreationForm

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Label created')
        return super(Create, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Label not created')
        return super(Create, self).form_invalid(form)

    def handle_no_permission(self):
        messages.error(self.request, 'Permission denied')
        return redirect('/')


class Update(LoginRequiredMixin, UpdateView):
    model = Label
    template_name = 'labels/update_label.html'
    success_url = '/labels/'
    fields = ['name']

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Label changed')
        return super(Update, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Label not changed')
        return super(Update, self).form_invalid(form)

    def handle_no_permission(self):
        messages.error(self.request, 'Permission denied')
        return redirect('/')


class Delete(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'labels/delete_label.html'
    success_url = '/labels/'

    def handle_no_permission(self):
        messages.error(self.request, 'Permission denied')
        return redirect('/')

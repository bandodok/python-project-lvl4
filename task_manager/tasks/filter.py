from task_manager.tasks.models import Task
from task_manager.labels.models import Label
import django_filters
from django.utils.translation import ugettext as _


class TaskFilter(django_filters.FilterSet):
    label = django_filters.ModelChoiceFilter(
        label=_('label'),
        queryset=Label.objects.all()
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'label']

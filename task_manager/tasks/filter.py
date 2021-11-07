from task_manager.tasks.models import Task
from task_manager.labels.models import Label
import django_filters


class TaskFilter(django_filters.FilterSet):
    labels = django_filters.ModelChoiceFilter(
        label='Метка',
        queryset=Label.objects.all(),
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']

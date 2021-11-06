from django.db import models
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


class Task(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(_('Name'), max_length=100)
    description = models.CharField(_('Description'), max_length=500)
    status = models.ForeignKey(Status, verbose_name=_('Status'), on_delete=models.CASCADE, related_name='status')
    author = models.ForeignKey(User, verbose_name=_('Author'), on_delete=models.CASCADE, related_name='author')
    executor = models.ForeignKey(User, verbose_name=_('Executor'), on_delete=models.CASCADE, related_name='executor')
    labels = models.ManyToManyField(Label, verbose_name=_('Labels'))

    def __str__(self):
        return self.name

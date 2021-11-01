from django.db import models
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from django.contrib.auth.models import User


class Task(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='status')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    executor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='executor')
    labels = models.ManyToManyField(Label)

    def __str__(self):
        return self.name

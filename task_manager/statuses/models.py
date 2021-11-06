from django.db import models
from django.utils.translation import ugettext as _


class Status(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(_('Name'), max_length=100)

    def __str__(self):
        return self.name

from django.db import models
from django.contrib.auth.models import User


def get_full_name(self):
    return f'{self.first_name} {self.last_name}'


User.add_to_class("__str__", get_full_name)


class Profile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)

    def __str__(self):
        return self.username.username

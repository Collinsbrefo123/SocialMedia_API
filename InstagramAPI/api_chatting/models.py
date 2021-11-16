from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Room(models.Model):
    room_name = models.CharField(max_length=1000)

    def __str__(self):
        return self.room_name


class Message(models.Model):
    value = models.CharField(max_length=100000)
    date = models.DateTimeField(default=datetime.now(), blank=True, null=True)
    user = models.CharField(max_length=100000)
    room = models.CharField(max_length=1000)

    def __str__(self):
        return self.user



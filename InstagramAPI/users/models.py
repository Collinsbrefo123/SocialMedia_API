from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=500)
    username = models.CharField(max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']


class Feeds(models.Model):
    feedTitle = models.CharField(max_length=100, null=True, blank=True)
    imgFeed = models.ImageField(upload_to='upload/images', blank=True)
    caption = models.TextField(max_length=500, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.feedTitle

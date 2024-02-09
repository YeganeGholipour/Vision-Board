from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    bio = models.CharField(max_length=255, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True, null=True)

    def __str__(self):
        return self.username


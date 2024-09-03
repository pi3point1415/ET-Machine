from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Meta:
        db_table = 'auth_user'
        ordering = ['username']

    def __str__(self):
        return self.username.upper()

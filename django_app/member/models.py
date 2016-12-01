from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


class UserManager(UserManager):
    pass

class MyUser(AbstractUser):
    nickname = models.CharField(max_length=50, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.nickname
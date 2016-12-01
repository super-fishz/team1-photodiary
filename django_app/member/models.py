from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


class UserManager(UserManager):
    pass

class MyUser(AbstractUser):



    def __str__(self):
        return self.username
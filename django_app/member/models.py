from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import ugettext_lazy as _


class UserManager(UserManager):
    pass

class MyUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)


    def __str__(self):
        return self.username
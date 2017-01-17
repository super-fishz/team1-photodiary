from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from versatileimagefield.fields import VersatileImageField


class UserManager(UserManager):
    pass


class MyUser(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=False,
    )
    profile_img = VersatileImageField('profile', upload_to='user_profile',  null=True, default=None)

    def __str__(self):
        return self.username

from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserManager(UserManager):
    pass

class MyUser(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=False,
        help_text=_('영문만 입력 가능 합니다.'),
        validators=[username_validator],
    )

    def __str__(self):
        return self.username

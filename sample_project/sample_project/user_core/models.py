from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    HELP_TEXTS = {
        'is_staff': _('Determines whether the user can log into the admin site.'),
    }

    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff status'), default=False, help_text=HELP_TEXTS['is_staff'])

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ('-is_active', 'last_name')

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    def get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)
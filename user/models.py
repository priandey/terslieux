from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **kwargs):

        if not username:
            raise ValueError('You must give an username')
        username = username
        user = self.model(username=username, **kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, username, password=None, **kwargs):
        kwargs.setdefault('is_superuser', False)
        return self._create_user(username, password, **kwargs)

    def create_superuser(self, username, password, **kwargs):
        kwargs.setdefault('is_superuser', True)

        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser Must have is_superuser=True')

        return self._create_user(username, password, **kwargs)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    User model with email instead of username/pseudo.
    """

    username = models.CharField(max_length=60, verbose_name=_('username'), unique=True)
    date_joined = models.DateTimeField(
        verbose_name=_('date_joined'), auto_now_add=True)
    is_active = models.BooleanField(verbose_name=_('active'), default=True)
    is_staff = models.BooleanField(verbose_name=_('admin'), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

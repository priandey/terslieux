from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **kwargs):

        if not email:
            raise ValueError('You must give an email')
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **kwargs):
        kwargs.setdefault('is_superuser', False)
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_superuser', True)

        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser Must have is_superuser=True')

        return self._create_user(email, password, **kwargs)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    '''
    User model with email instead of username/pseudo.
    '''

    email = models.EmailField(verbose_name=_('email'), unique=True)
    date_joined = models.DateTimeField(
        verbose_name=_('date_joined'), auto_now_add=True)
    is_active = models.BooleanField(verbose_name=_('active'), default=True)
    is_staff = models.BooleanField(verbose_name=_('admin'), default=False)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Volunteer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class Moderator(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, unique=True)

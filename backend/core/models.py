from django.db import models
from django.contrib.auth.models import (
  AbstractBaseUser,
  BaseUserManager,
  PermissionsMixin,
)


class UserManager(BaseUserManager):
  def create_user(self, username, email, password=None, **extra_fields):
    user = self.model(username=username, email=self.normalize_email(email),
                      **extra_fields)
    user.set_password(password)
    user.save(using=self._db)

    return user

  def create_superuser(self, username, email='admin@example.com', password=None,
                       **extra_fields):
    user = self.create_user(username, email, password, **extra_fields)
    user.is_staff = True
    user.is_superuser = True

    user.save(using=self._db)

    return user


class User(AbstractBaseUser, PermissionsMixin):
  username = models.CharField(max_length=255, unique=True)
  email = models.EmailField(max_length=255, unique=True)
  name = models.CharField(max_length=255)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)

  objects = UserManager()

  USERNAME_FIELD = 'username'

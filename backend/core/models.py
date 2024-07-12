from datetime import timedelta, datetime
from django.contrib.auth.models import (
  AbstractBaseUser,
  BaseUserManager,
  PermissionsMixin,
)
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from django.db import models


def validate_date_format(value):
  try:
    datetime.strptime(str(value), '%Y-%m-%d')
  except ValueError:
    raise ValidationError(_('Invalid date format. Use YYYY-MM-DD.'))


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


class Election(models.Model):
  title = models.CharField(max_length=255, unique=True)
  slug = models.SlugField(max_length=255, unique=True, blank=True)
  start_date = models.DateField()
  end_date = models.DateField()

  def clean(self):
    super().clean()
    if self.end_date <= self.start_date:
      raise ValidationError(_('End date must be after start date.'))
    if (self.end_date - self.start_date) < timedelta(days=1):
      raise ValidationError(_('The election must last at least 1 day.'))

  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = slugify(self.title)
    validate_date_format(self.start_date)
    validate_date_format(self.end_date)
    self.full_clean()
    super().save(*args, **kwargs)

  def __str__(self):
    return self.title


class Candidate(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  election = models.ForeignKey(Election, on_delete=models.CASCADE)
  description = models.CharField(max_length=255)

  class Meta:
    unique_together = ('user', 'election')

  def __str__(self):
    return f'{self.user} - {self.election.slug}'


class Vote(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  election = models.ForeignKey(Election, on_delete=models.CASCADE)
  voted_candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

  class Meta:
    unique_together = ('user', 'election')

  def clean(self):
    super().clean()
    if self.voted_candidate.election != self.election:
      raise ValidationError(
        'The voted candidate must belong to the specified election.'
      )

  def save(self, *args, **kwargs):
    self.full_clean()
    return super().save(*args, **kwargs)

  def __str__(self):
    return f'{self.user.username} voted in {self.election.title} ' + \
      f'for {self.voted_candidate.user.username}'

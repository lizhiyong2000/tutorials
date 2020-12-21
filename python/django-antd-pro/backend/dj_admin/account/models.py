from django.db import models

# Create your models here.

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
# from django.forms import models
from django.shortcuts import render

# Create your views here.
from django.utils import timezone


class DeviceUser(AbstractBaseUser):
    username = models.CharField(
        unique=True,
        max_length=254,
    )
    sn = models.CharField(max_length=15)

    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    # objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['sn']

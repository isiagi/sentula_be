from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
import re

from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
            
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must have is_active=True.')

        return self.create_user(username=username, email=email, password=password, **extra_fields)


class CustomUser(AbstractUser):
    objects = CustomUserManager()

    username = models.CharField(
        max_length=150, 
        unique=True,
        help_text='Required. 150 characters or fewer. Letters, digits, and spaces only.',
        validators=[],
        error_messages={
            'unique': "A Member with that Membership ID already exists.",
        },
    )

    otp = models.CharField(max_length=150, null=True, blank=True)

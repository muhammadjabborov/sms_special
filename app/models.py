from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager
from django.db.models import Model, EmailField, ImageField, CharField, DateTimeField
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import models


class BaseModel(Model):
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)


class User(AbstractUser, PermissionsMixin):
    activation_code = models.CharField(max_length=4)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email


class Image(BaseModel):
    icon = ImageField(upload_to='icons/')
    title = CharField(max_length=255)

    def __str__(self):
        return self.title

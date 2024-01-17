from django.contrib.auth.models import AbstractUser
from django.db import models
from django_userforeignkey.models.fields import UserForeignKey

from app_aggregator.model_choices import UserTypes


class User(AbstractUser):
    type = models.PositiveSmallIntegerField(choices=UserTypes.choices)


class AppData(models.Model):
    url = models.URLField()
    created_by = UserForeignKey(auto_user_add=True, related_name="%(class)s_create")
    name = models.CharField(max_length=100)
    description = models.TextField()
    active = models.BooleanField(default=True)


class UserPurchasedApps(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchased_app')
    app = models.ForeignKey(AppData, on_delete=models.PROTECT, related_name='user_apps')
    active = models.BooleanField(default=True)

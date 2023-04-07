from django.contrib.auth.models import User
from django.db import models

from register_tel.settings import MEDIA_ROOT


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_account")
    telegram_id = models.IntegerField(unique=True)
    nick_name = models.CharField(unique=True, max_length=100)
    photo_url = models.FilePathField(path=MEDIA_ROOT, null=True, blank=True)

    def __str__(self):
        return self.user.username

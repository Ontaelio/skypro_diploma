from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class TgUser(models.Model):
    class Meta:
        verbose_name = 'TG юзер'
        verbose_name_plural = 'TG юзеры'

    tg_user = models.IntegerField(unique=True, verbose_name="Пользователь TG")
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, verbose_name="Пользователь")
    verification_code = models.CharField(max_length=10, null=True, blank=True)




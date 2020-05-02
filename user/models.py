from django.contrib.auth.models import AbstractUser, Group
from django.db import models


class User(AbstractUser):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    email_token = models.CharField('Токен для подтверждения почты', max_length=32, blank=True)
    is_email_confirmed = models.BooleanField('Email подтвержден?', default=False)


class UserGroup(Group):
    class Meta:
        proxy = True
        verbose_name = 'Группа пользователей'
        verbose_name_plural = 'Группы пользователей'

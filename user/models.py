import random
import string

from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    email = models.EmailField(_('email address'), blank=True, unique=True)
    email_token = models.CharField(verbose_name='Токен для подтверждения почты', max_length=32, blank=True)
    is_email_confirmed = models.BooleanField(verbose_name='Email подтвержден?', default=False)

    def generate_email_token(self, *, commit=True) -> str:
        """
            Генерирует email токен для подтверждения и делает пользователя неактивным
        :param commit: заносить изменения в БД или нет
        :return: Сгенерированный токен
        """
        token = random.choices(string.ascii_letters + string.digits, k=32)
        token = ''.join(token)
        self.email_token = token
        self.is_email_confirmed = False
        self.is_active = False
        if commit:
            self.save(update_fields=['email_token', 'is_email_confirmed', 'is_active'])
        return token


class UserSettings(models.Model):
    class Meta:
        verbose_name = 'Настройки пользователя'
        verbose_name_plural = 'Настройки пользователей'

    user = models.OneToOneField(User, verbose_name='Пользователь', on_delete=models.CASCADE, related_name='settings')


class UserGroup(Group):
    class Meta:
        proxy = True
        verbose_name = 'Группа пользователей'
        verbose_name_plural = 'Группы пользователей'


@receiver(post_save, sender=User)
def user_post_save(**kwargs):
    # Для каждого созданного юзера создаем "настройки"
    if kwargs['created']:
        UserSettings.objects.create(user=kwargs['instance'])


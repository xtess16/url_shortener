from django.db import models

from user.models import User


class URL(models.Model):
    class Meta:
        verbose_name = 'Ссылка'
        verbose_name_plural = 'Ссылки'

    owner = models.OneToOneField(User, verbose_name='Владелец', on_delete=models.CASCADE)
    full_link = models.CharField(verbose_name='Исходная ссылка', max_length=65536)
    short_link = models.CharField(verbose_name='Сокращенная ссылка', max_length=64)


class Transition(models.Model):
    class Meta:
        verbose_name = 'Переход по ссылке'
        verbose_name_plural = 'Переходы по ссылкам'

    ip = models.CharField(verbose_name='IP', max_length=40)
    url = models.OneToOneField(URL, verbose_name='URL', on_delete=models.CASCADE)
    transition_date = models.DateTimeField(verbose_name='Дата и время перехода')
    location = models.CharField(verbose_name='Локация', max_length=256)

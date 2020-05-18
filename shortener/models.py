from django.db import models

from user.models import User
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save
from core.settings import GEO_LOCATOR


class URL(models.Model):
    class Meta:
        verbose_name = 'Ссылка'
        verbose_name_plural = 'Ссылки'

    owner = models.ForeignKey(User, verbose_name='Владелец', on_delete=models.CASCADE)
    full_link = models.CharField(verbose_name='Исходная ссылка', max_length=65536)
    short_link = models.CharField(verbose_name='Сокращенная ссылка', max_length=64)


class Transition(models.Model):
    class Meta:
        verbose_name = 'Переход по ссылке'
        verbose_name_plural = 'Переходы по ссылкам'

    ip = models.CharField(verbose_name='IP', max_length=40)
    url = models.OneToOneField(URL, verbose_name='URL', on_delete=models.CASCADE)
    transition_date = models.DateTimeField(verbose_name='Дата и время перехода')
    latitude = models.FloatField(verbose_name='Широта', null=True)
    longitude = models.FloatField(verbose_name='Долгота', null=True)
    country = models.CharField(verbose_name='Страна', max_length=64, blank=True)
    region = models.CharField(verbose_name='Регион', max_length=128, blank=True)
    city = models.CharField(verbose_name='Населенный пункт', max_length=128, blank=True)


@receiver(post_save, sender=Transition)
def transition_post_save(**kwargs):
    if GEO_LOCATOR is not None and kwargs['created']:
        instance = kwargs['instance']
        if (location := GEO_LOCATOR.get_location(instance.ip, detailed=True)) is not None:
            info = location['info']
            instance.latitude = location['lat']
            instance.longitude = location['lon']
            instance.country = info['country']['name_ru']
            instance.region = info['region']['name_ru']
            instance.city = info['city']['name_ru']
            instance.save(update_fields=['latitude', 'longitude', 'country', 'region', 'city'])

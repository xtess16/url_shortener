import random
import string
from urllib.parse import urljoin

import pytz
from django.db import models

from core import settings
from core.settings import GEO_LOCATOR
from user.models import User


class URL(models.Model):
    class Meta:
        verbose_name = 'Ссылка'
        verbose_name_plural = 'Ссылки'

    short_link_length = 9
    owner = models.ForeignKey(User, verbose_name='Владелец', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Заголовок', max_length=128)
    full_link = models.CharField(verbose_name='Исходная ссылка', max_length=65536)
    short_link = models.CharField(verbose_name='Сокращенная ссылка', max_length=64)
    description = models.TextField(verbose_name='Описание', blank=True, default='')
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)

    def generate_short_link(self, *, commit=False) -> str:
        """
            Генерирует короткую ссылку
        :param commit: заносить изменения в БД или нет
        :return: сгенерированная ссылка
        """
        short_link = ''.join(random.choices(string.ascii_letters + string.digits, k=self.short_link_length))
        self.short_link = short_link
        if commit:
            self.save(update_fields=['short_link'])
        return short_link

    @property
    def short_link_with_hostname(self):
        return urljoin(settings.HOSTNAME, 'r/') + self.short_link

    def __str__(self):
        return f'{self.title} ({self.owner})'


class Transition(models.Model):
    class Meta:
        verbose_name = 'Переход по ссылке'
        verbose_name_plural = 'Переходы по ссылкам'

    ip = models.CharField(verbose_name='IP', max_length=40, blank=True)
    url = models.ForeignKey(URL, verbose_name='URL', on_delete=models.CASCADE)
    transition_datetime = models.DateTimeField(verbose_name='Дата и время перехода', auto_now_add=True)
    latitude = models.FloatField(verbose_name='Широта', null=True)
    longitude = models.FloatField(verbose_name='Долгота', null=True)
    country = models.CharField(verbose_name='Страна', max_length=64, blank=True)
    region = models.CharField(verbose_name='Регион', max_length=128, blank=True)
    city = models.CharField(verbose_name='Населенный пункт', max_length=128, blank=True)

    def set_location(self, commit=True):
        if GEO_LOCATOR is None or not self.ip:
            return
        try:
            location = GEO_LOCATOR.get_location(self.ip, detailed=True)
            if not location:
                raise ValueError
        except ValueError:
            return
        else:
            info = location['info']
            lat, lon = location['lat'], location['lon']
            country = info['country']['name_ru']
            region = info['region']['name_ru']
            city = info['city']['name_ru']
            self.latitude = lat
            self.longitude = lon
            self.country = country
            self.region = region
            self.city = city
            if commit:
                self.save(update_fields=['latitude', 'longitude', 'country', 'region', 'city'])
            return lat, lon, country, region, city

    def __str__(self):
        transition_datetime = self.transition_datetime.astimezone(pytz.timezone(settings.TIME_ZONE))
        return f'{self.url.short_link_with_hostname} ({transition_datetime.ctime()})'


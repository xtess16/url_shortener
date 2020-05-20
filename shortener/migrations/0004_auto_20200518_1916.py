# Generated by Django 3.0.5 on 2020-05-18 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortener', '0003_auto_20200518_0046'),
    ]

    operations = [
        migrations.AddField(
            model_name='url',
            name='description',
            field=models.TextField(blank=True, default='', verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='url',
            name='title',
            field=models.CharField(default='Title', max_length=128, verbose_name='Заголовок'),
            preserve_default=False,
        ),
    ]
# Generated by Django 3.0.5 on 2020-05-22 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortener', '0009_auto_20200519_2000'),
    ]

    operations = [
        migrations.AddField(
            model_name='transition',
            name='user_agent',
            field=models.CharField(blank=True, max_length=1024, verbose_name='User Agent'),
        ),
    ]
# Generated by Django 3.0.5 on 2020-05-19 16:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shortener', '0007_auto_20200519_1948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transition',
            name='url',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shortener.URL', verbose_name='URL'),
        ),
    ]
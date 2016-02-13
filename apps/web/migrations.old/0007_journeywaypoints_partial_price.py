# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-12 09:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0006_auto_20160212_0921'),
    ]

    operations = [
        migrations.AddField(
            model_name='journeywaypoints',
            name='partial_price',
            field=models.FloatField(blank=True, default=None, null=True, verbose_name='Price between previous and this waypoint (currency is same).'),
        ),
    ]
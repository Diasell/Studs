# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-29 10:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0002_auto_20160629_1031'),
    ]

    operations = [
        migrations.AddField(
            model_name='workingday',
            name='dayoftheweeknumber',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
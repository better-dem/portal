# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-01-13 02:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_auto_20170113_0204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participationproject',
            name='name',
            field=models.CharField(max_length=500),
        ),
    ]

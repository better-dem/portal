# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-01-13 02:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_event_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participationitem',
            name='name',
            field=models.CharField(max_length=500),
        ),
    ]
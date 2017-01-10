# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-01-10 20:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='participationitem',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='participationproject',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
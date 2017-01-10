# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-01-04 20:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20170103_1607'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participationitem',
            name='display_image_url',
        ),
        migrations.AddField(
            model_name='participationitem',
            name='display_image_file',
            field=models.FilePathField(blank=True, max_length=500),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-10-23 23:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_participationproject_owner_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='participationitem',
            name='display_image_url',
            field=models.URLField(blank=True),
        ),
    ]

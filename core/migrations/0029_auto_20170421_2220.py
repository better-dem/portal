# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-04-21 22:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_auto_20170421_1930'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedmatch',
            name='participation_item',
        ),
        migrations.RemoveField(
            model_name='feedmatch',
            name='user_profile',
        ),
        migrations.DeleteModel(
            name='FeedMatch',
        ),
    ]

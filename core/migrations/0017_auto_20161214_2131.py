# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-12-14 21:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_userprofile_sessions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='is_temporary',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='sessions',
        ),
    ]

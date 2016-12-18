# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-11-27 05:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sessions', '0001_initial'),
        ('core', '0015_userprofile_is_temporary'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='sessions',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sessions.Session'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-23 19:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_auto_20170523_0543'),
    ]

    operations = [
        migrations.AddField(
            model_name='participationproject',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.UserGroup'),
        ),
    ]
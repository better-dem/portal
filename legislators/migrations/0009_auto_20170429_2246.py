# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-04-29 22:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legislators', '0008_auto_20170429_2203'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='billsitem',
            options={'get_latest_by': 'last_action_date'},
        ),
        migrations.AlterModelOptions(
            name='billsproject',
            options={},
        ),
        migrations.AddField(
            model_name='billsitem',
            name='last_action_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
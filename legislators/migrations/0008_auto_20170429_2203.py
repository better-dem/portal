# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-04-29 22:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('legislators', '0007_billsproject_documents'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='billsproject',
            options={'get_latest_by': 'last_action_date'},
        ),
    ]

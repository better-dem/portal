# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-04-14 20:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legislators', '0003_auto_20170414_2000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='legislatorsproject',
            name='chamber',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
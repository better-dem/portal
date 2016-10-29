# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-10-28 23:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20161028_2250'),
    ]

    operations = [
        migrations.AddField(
            model_name='geotag',
            name='feature_type',
            field=models.CharField(choices=[('CO', 'Country'), ('SP', 'State or Province'), ('CI', 'City or town'), ('OT', 'Other'), ('UN', 'Unknown')], default='UN', max_length=2),
        ),
    ]

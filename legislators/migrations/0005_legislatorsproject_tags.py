# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-04-14 20:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_donation'),
        ('legislators', '0004_auto_20170414_2013'),
    ]

    operations = [
        migrations.AddField(
            model_name='legislatorsproject',
            name='tags',
            field=models.ManyToManyField(to='core.Tag'),
        ),
    ]

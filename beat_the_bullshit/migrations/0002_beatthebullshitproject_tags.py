# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-03-09 05:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_donation'),
        ('beat_the_bullshit', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='beatthebullshitproject',
            name='tags',
            field=models.ManyToManyField(to='core.Tag'),
        ),
    ]
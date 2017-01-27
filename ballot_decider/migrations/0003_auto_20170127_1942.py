# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-01-27 19:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_auto_20170113_0205'),
        ('ballot_decider', '0002_auto_20170125_1813'),
    ]

    operations = [
        migrations.AddField(
            model_name='ballotdeciderproject',
            name='basics_notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='ballotdeciderproject',
            name='effects',
            field=models.ManyToManyField(related_name='_ballotdeciderproject_effects_+', to='core.ParticipationItem'),
        ),
        migrations.AddField(
            model_name='ballotdeciderproject',
            name='effects_notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]
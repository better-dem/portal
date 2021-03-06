# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-02-08 20:58
from __future__ import unicode_literals

import core.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_auto_20170113_0205'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shortcut',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shortcut_string', models.CharField(max_length=500, unique=True, validators=[core.models.validate_shortcut_string])),
                ('target_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.ParticipationItem')),
            ],
        ),
    ]

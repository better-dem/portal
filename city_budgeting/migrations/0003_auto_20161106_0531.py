# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-11-06 05:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('city_budgeting', '0002_service'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='expected_expenditure',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]

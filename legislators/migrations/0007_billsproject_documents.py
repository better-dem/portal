# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-04-25 21:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0030_referencedocument'),
        ('legislators', '0006_billsitem_billsproject'),
    ]

    operations = [
        migrations.AddField(
            model_name='billsproject',
            name='documents',
            field=models.ManyToManyField(to='core.ReferenceDocument'),
        ),
    ]

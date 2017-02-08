# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-02-08 00:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_auto_20170113_0205'),
        ('manual_news_article_curation', '0002_auto_20161021_1906'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='manualnewscurationproject',
            name='img_url',
        ),
        migrations.AddField(
            model_name='manualnewscurationproject',
            name='screenshot_filename',
            field=models.FilePathField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='manualnewscurationproject',
            name='tags',
            field=models.ManyToManyField(to='core.Tag'),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-01-03 17:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0018_auto_20170103_1607'),
    ]

    operations = [
        migrations.CreateModel(
            name='ToolReviewItem',
            fields=[
                ('participationitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.ParticipationItem')),
            ],
            bases=('core.participationitem',),
        ),
        migrations.CreateModel(
            name='ToolReviewProject',
            fields=[
                ('participationproject_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.ParticipationProject')),
                ('url', models.URLField()),
                ('screenshot', models.FileField(upload_to=b'')),
                ('summary', models.TextField()),
                ('review_video', models.URLField(blank=True)),
                ('review_blog_post', models.URLField(blank=True)),
                ('tags', models.ManyToManyField(to='core.Tag')),
            ],
            bases=('core.participationproject',),
        ),
    ]

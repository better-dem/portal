# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-01-17 18:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0024_auto_20170113_0205'),
    ]

    operations = [
        migrations.CreateModel(
            name='BallotDeciderItem',
            fields=[
                ('participationitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.ParticipationItem')),
            ],
            bases=('core.participationitem',),
        ),
        migrations.CreateModel(
            name='BallotDeciderProject',
            fields=[
                ('participationproject_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.ParticipationProject')),
                ('ballot_text', models.TextField()),
                ('election_date', models.DateField()),
                ('election_website', models.URLField()),
                ('basics', models.ManyToManyField(to='core.ParticipationItem')),
            ],
            bases=('core.participationproject',),
        ),
        migrations.CreateModel(
            name='PointOfView',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quote', models.TextField()),
                ('citation_url', models.URLField()),
                ('favorability', models.FloatField()),
            ],
        ),
        migrations.AddField(
            model_name='ballotdeciderproject',
            name='points_of_view',
            field=models.ManyToManyField(to='ballot_decider.PointOfView'),
        ),
        migrations.AddField(
            model_name='ballotdeciderproject',
            name='tags',
            field=models.ManyToManyField(to='core.Tag'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-19 23:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0031_auto_20170515_2224'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderedAssignmentItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ReadingAssignmentItem',
            fields=[
                ('participationitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.ParticipationItem')),
            ],
            bases=('core.participationitem',),
        ),
        migrations.CreateModel(
            name='ReadingAssignmentProject',
            fields=[
                ('participationproject_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.ParticipationProject')),
            ],
            bases=('core.participationproject',),
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('participation_project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reading_assignment.ReadingAssignmentProject')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='TextQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='TextQuestionResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response', models.TextField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reading_assignment.TextQuestion')),
                ('submission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reading_assignment.Submission')),
            ],
        ),
        migrations.AddField(
            model_name='orderedassignmentitem',
            name='assignment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reading_assignment.ReadingAssignmentProject'),
        ),
        migrations.AddField(
            model_name='orderedassignmentitem',
            name='participation_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.ParticipationItem'),
        ),
        migrations.AddField(
            model_name='orderedassignmentitem',
            name='text_question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reading_assignment.TextQuestion'),
        ),
    ]
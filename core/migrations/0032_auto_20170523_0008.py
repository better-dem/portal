# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-23 00:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_auto_20170515_2224'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupMembership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member_name', models.CharField(max_length=100)),
                ('invitation_code', models.CharField(max_length=100)),
                ('invitation_email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('group_type', models.CharField(choices=[('Course', 'Course')], default='Course', max_length=50)),
                ('max_invitations', models.PositiveIntegerField(default=25)),
            ],
        ),
        migrations.AddField(
            model_name='userprofile',
            name='role',
            field=models.CharField(choices=[('Teacher', 'Teacher'), ('Student', 'Student'), ('Journalist', 'Journalist'), ('Ordinary Citizen', 'Ordinary Citizen')], default='Ordinary Citizen', max_length=50),
        ),
        migrations.AddField(
            model_name='usergroup',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.UserProfile'),
        ),
        migrations.AddField(
            model_name='groupmembership',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.UserGroup'),
        ),
        migrations.AddField(
            model_name='groupmembership',
            name='member',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.UserProfile'),
        ),
    ]

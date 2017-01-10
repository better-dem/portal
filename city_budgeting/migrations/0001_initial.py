# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-11-05 23:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0013_participationitem_creation_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='CityBudgetingProject',
            fields=[
                ('participationproject_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.ParticipationProject')),
                ('fiscal_year_end_date', models.DateField()),
                ('total_expected_revenue', models.PositiveIntegerField()),
                ('total_expected_expenditure', models.PositiveIntegerField()),
                ('mayor_name', models.CharField(max_length=100)),
                ('council_members', models.TextField()),
                ('budget_url', models.URLField()),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.GeoTag')),
            ],
            bases=('core.participationproject',),
        ),
        migrations.CreateModel(
            name='CityBudgetQuiz',
            fields=[
                ('participationitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.ParticipationItem')),
            ],
            bases=('core.participationitem',),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='QuizResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('participation_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='city_budgeting.CityBudgetQuiz')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='TMCQ',
            fields=[
                ('question_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='city_budgeting.Question')),
                ('option1', models.CharField(max_length=100)),
                ('option2', models.CharField(max_length=100)),
                ('option3', models.CharField(max_length=100)),
                ('option4', models.CharField(max_length=100)),
                ('option5', models.CharField(max_length=100)),
                ('correct_answer_index', models.IntegerField()),
            ],
            bases=('city_budgeting.question',),
        ),
        migrations.CreateModel(
            name='TMCQResponse',
            fields=[
                ('questionresponse_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='city_budgeting.QuestionResponse')),
                ('option_index', models.IntegerField()),
            ],
            bases=('city_budgeting.questionresponse',),
        ),
        migrations.AddField(
            model_name='questionresponse',
            name='item_response',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='city_budgeting.QuizResponse'),
        ),
        migrations.AddField(
            model_name='questionresponse',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='city_budgeting.Question'),
        ),
        migrations.AddField(
            model_name='question',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='city_budgeting.CityBudgetQuiz'),
        ),
    ]
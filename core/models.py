from __future__ import unicode_literals
from django.db import models

class ParticipationProject(models.Model):
    name = models.CharField(max_length = 100)

class ParticipationItem(models.Model):
    name = models.CharField(max_length = 100)
    participation_project = models.ForeignKey('ParticipationProject', on_delete=models.CASCADE)

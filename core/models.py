from __future__ import unicode_literals
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

class ParticipationProject(models.Model):
    name = models.CharField(max_length = 100)

class ParticipationItem(models.Model):
    name = models.CharField(max_length = 100)
    participation_project = models.ForeignKey('ParticipationProject', on_delete=models.CASCADE)

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

class FeedMatch(models.Model):
    participation_item = models.ForeignKey('ParticipationItem', on_delete = models.CASCADE)
    user_profile = models.ForeignKey('UserProfile', on_delete = models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True)


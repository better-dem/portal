from __future__ import unicode_literals
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User


# registered participation apps
# ParticipationApp class and the registration function
# can be found in ./ParticipationApp.py
# apps need to be registered in order for them to be 
# displayed and managed correctly by the portal core app
registered_apps = []

class ParticipationProject(models.Model):
    name = models.CharField(max_length = 100)

class ParticipationItem(models.Model):
    name = models.CharField(max_length = 100)
    participation_project = models.ForeignKey('ParticipationProject', on_delete=models.CASCADE)

    def get_inherited_instance(self):
        ans = self
        for t in [app.item_subclass_test for app in registered_apps]:
            try:
                ans = t(self)
            except:
                continue
            else:
                return ans
        raise Exception("unknown subclass type")

    def get_description(self):
        return self.name + " participation item"



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


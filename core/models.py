from __future__ import unicode_literals
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

# functions to return the appropriate subclass of a participation item 
# or raise an exception
# assumes only one level of inheritance
# NOTE: every class which inherits from ParticipationItem needs to register a test
# for example: core.models.participation_item_subclass_tests.append(lambda x: x.dummyitem)

participation_item_subclass_tests = []



class ParticipationProject(models.Model):
    name = models.CharField(max_length = 100)

class ParticipationItem(models.Model):
    name = models.CharField(max_length = 100)
    participation_project = models.ForeignKey('ParticipationProject', on_delete=models.CASCADE)

    def get_inherited_instance(self):
        ans = self
        for t in participation_item_subclass_tests:
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


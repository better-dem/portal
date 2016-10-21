from __future__ import unicode_literals
from django.db import models, transaction
from django.db.models.signals import post_save
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.apps import apps

### Start functions for accessing particpation app API
def get_registered_participation_apps():
    import sys
    all_apps = apps.get_app_configs()
    participation_apps = [a for a in all_apps if not a.name=="core" and len(get_app_project_models(a))==1]
    return participation_apps

def get_app_project_models(app):
    return [m for m in app.get_models() if issubclass(m, ParticipationProject)]
    
def get_item_subclass_test(app):
    item_models = [m for m in app.get_models() if issubclass(m, ParticipationItem)]
    if len(item_models) == 0:
        raise Exception("app"+app.name+" has no Participation Item models")
    m = item_models[0]
    subclass_name = m.__name__.lower().replace("_","")
    return lambda x: getattr(x, subclass_name)

def get_provider_permission(app):
    # create a Permission object if there isn't one yet
    project_model = get_app_project_models(app)[0]
    content_type = ContentType.objects.get(app_label="core", model=project_model.__name__.lower().replace("_",""))
    try:
        perm = Permission.objects.get(content_type=content_type)
        return perm
    except Permission.DoesNotExist:
        perm = Permission()
        perm.name = "provider_permission_"+app.label
        perm.content_type = content_type
        perm.codename =  "permission_"+app.label
        perm.save()
        return perm

def get_provider_permission_name(app):
    return "provider_permission_"+app.label


### Start core models
class ParticipationProject(models.Model):
    name = models.CharField(max_length = 100)
    owner_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE)

class ParticipationItem(models.Model):
    name = models.CharField(max_length = 100)
    participation_project = models.ForeignKey('ParticipationProject', on_delete=models.CASCADE)

    def get_inherited_instance(self):
        ans = self
        for t in [get_item_subclass_test(app) for app in get_registered_participation_apps()]:
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



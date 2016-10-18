"""
ParticipationApp class

In each BetterDem Portal Participation app's models file, 
a ParticipationApp object should be created to register that app with the core app.

"""

from django.contrib.auth.models import Permission
import models
import sys

forbidden_app_names = {"", "admin", "accounts"}

def register(app):
    existing_app_names = set([x.app_name for x in models.registered_apps])
    if app.app_name in existing_app_names:
        raise Exception("can't register app with duplicate names: "+str(app.app_name))
    if app.app_name in forbidden_app_names:
        raise Exception("can't register app with a forbidden name: \""+str(app.app_name))+"\""
    models.registered_apps.append(app)

    if ('makemigrations' in sys.argv or 'migrate' in sys.argv):
        return 
    else:
        try:
            perm = Permission.objects.get(name=app.provider_permission_name())[0]
        except Permission.DoesNotExist:
            perm = Permission()
            perm.name = app.provider_permission_name()
            perm.save()


class ParticipationApp:
    def __init__(self, app_name, project_class_manager, item_subclass_test, views_module):
        """
        app_name:
        a unique name for this app.
        stick with letters, numbers, underscores
        no spaces or weird characters that might mess up a url or html

        project_class_manager:
        manager for this app's project class

        item_subclass_test:
        function to return the appropriate subclass of core.ParticipationItem 
        or raise an exception
        assumes only one level of inheritance

        views_module
        the views module for this app.
        Must include:
         - new_project(request)
         - show_project_results(request, project_id)
         - administer_project(request, project_id)
         - participate(request, item_id)
        """
        self.app_name = app_name
        self.project_class_manager = project_class_manager
        self.item_subclass_test = item_subclass_test
        self.views_module = views_module

    def provider_permission_name(app):
        return "provider_permission_"+app.app_name

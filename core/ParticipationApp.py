"""
ParticipationApp class

In each BetterDem Portal Participation app's models file, 
a ParticipationApp object should be created to register that app with the core app.

"""

import models

def register(app):
    models.registered_apps.append(app)

class ParticipationApp:
    def __init__(self, item_subclass_test, provider_permission):
        """
        item_subclass_test:
        function to return the appropriate subclass of core.ParticipationItem 
        or raise an exception
        assumes only one level of inheritance

        provider_permission:
        the django.contrib.auth.models.Permission object which gives
        users permission to create and administer their content for an app
        """
        self.item_subclass_test = item_subclass_test
        self.provider_permission = provider_permission


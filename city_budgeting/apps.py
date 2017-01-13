from __future__ import unicode_literals
from django.apps import AppConfig
from django.utils.module_loading import module_has_submodule
from importlib import import_module

class CityBudgetingConfig(AppConfig):
    name = 'city_budgeting'
    are_projects_editable = False
    custom_feed_item_template = None

    def ready(self):
        if module_has_submodule(self.module, "views"):
            views_module_name = '%s.%s' % (self.name, "views")
            self.views_module = import_module(views_module_name)

        from . import models
        from core import models as cm
        item_classes = [cls for name, cls in models.__dict__.items() if isinstance(cls, type) and issubclass(cls, cm.ParticipationItem)]
        for c in item_classes:
            cm.register_participation_item_subclass(c)
        
        from core import tasks as ct
        project_classes = [cls for name, cls in models.__dict__.items() if isinstance(cls, type) and issubclass(cls, cm.ParticipationProject)]
        for c in project_classes:
            ct.register_participation_project_subclass(c)

from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.module_loading import module_has_submodule
from importlib import import_module


class ToolReviewConfig(AppConfig):
    name = 'tool_review'
    are_projects_editable = True
    custom_feed_item_template = None
    external_link=False
    overviews = [[-1, "External Tool Database"],]
    creator_user_roles_allowed = ["Journalist"]

    def ready(self):
        if module_has_submodule(self.module, "views"):
            views_module_name = '%s.%s' % (self.name, "views")
            self.views_module = import_module(views_module_name)

        from . import models
        from core import models as cm
        item_classes = [cls for name, cls in models.__dict__.items() if isinstance(cls, type) and issubclass(cls, cm.ParticipationItem)]
        for c in item_classes:
            cm.register_participation_item_subclass(c)
        

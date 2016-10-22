from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.module_loading import module_has_submodule
from importlib import import_module


class DummyParticipationProjectConfig(AppConfig):
    name = 'dummy_participation_project'

    def ready(self):
        if module_has_submodule(self.module, "views"):
            views_module_name = '%s.%s' % (self.name, "views")
            self.views_module = import_module(views_module_name)

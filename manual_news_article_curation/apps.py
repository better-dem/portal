from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.module_loading import module_has_submodule
from importlib import import_module

class ManualNewsArticleCurationConfig(AppConfig):
    name = 'manual_news_article_curation'

    def ready(self):
        if module_has_submodule(self.module, "views"):
            views_module_name = '%s.%s' % (self.name, "views")
            self.views_module = import_module(views_module_name)

from __future__ import unicode_literals
from django.db import models

from core import models as cm
from core import ParticipationApp as cp
from . import views as views_module

class ManualNewsCurationProject(cm.ParticipationProject):
    pass

class NewsArticleItem(cm.ParticipationItem):
    url = models.URLField(blank=False)
    img_url = models.URLField(blank=False)
    first_paragraph = models.TextField(blank=False)

    def get_description(self):
        return self.first_paragraph[:300]+"..."

# register NewsArticleItem with core app
cp.register(cp.ParticipationApp("ManualNewsCurationApp", ManualNewsCurationProject, lambda x: x.newsarticleitem, views_module))

from __future__ import unicode_literals
from django.db import models

from core import models as cm

class ManualNewsCurationProject(cm.ParticipationProject):
    url = models.URLField(blank=False)
    img_url = models.URLField(blank=False)
    first_paragraph = models.TextField(blank=False)

class NewsArticleItem(cm.ParticipationItem):
    def get_description(self):
        return self.participation_project.manualnewscurationproject.first_paragraph[:300]+"..."


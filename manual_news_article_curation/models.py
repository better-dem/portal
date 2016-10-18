from __future__ import unicode_literals
from django.db import models

from core import models as cm
from core import ParticipationApp as cp

# register NewsArticleItem with core app
cp.register(cp.ParticipationApp(lambda x: x.newsarticleitem))

class ManualNewsCurationProject(cm.ParticipationProject):
    pass


class NewsArticleItem(cm.ParticipationItem):
    url = models.URLField(required=True)
    img_url = models.URLField(required=True)
    first_paragraph = models.TextField(required=True)

    def get_description(self):
        return self.first_paragraph[:300]+"..."


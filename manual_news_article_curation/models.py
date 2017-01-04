from __future__ import unicode_literals
from django.contrib.gis.db import models

from core import models as cm

org_logos = dict()
org_logos["ballotpedia.org"] = "manual_news_article_curation/img/bp-logo.svg"
org_logos["challenge.gov"] = "manual_news_article_curation/img/challenge_full_logo.png"

class ManualNewsCurationProject(cm.ParticipationProject):
    url = models.URLField(blank=False)
    img_url = models.URLField(blank=False)
    first_paragraph = models.TextField(blank=False)

    def update_items(self):
        if NewsArticleItem.objects.filter(participation_project=self).count() == 0:
            item = NewsArticleItem()
            item.name = self.name
            item.participation_project = self
            item.save()
            return set([item.id])
        return set()

class NewsArticleItem(cm.ParticipationItem):
    def get_description(self):
        return self.participation_project.manualnewscurationproject.first_paragraph[:300]+"..."

    def set_display_image(self):
        for org in org_logos:
            if org in self.participation_project.url:
                self.display_image_file = org_logos[org]
                return
        self.display_image_file = 'manual_news_article_curation/img/default.png'

    def set_relevant_tags(self):
        # i should do some NLP or something...
        self.tags.add(cm.get_usa())

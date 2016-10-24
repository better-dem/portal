from __future__ import unicode_literals
from django.db import models

from core import models as cm

org_logos = dict()
org_logos["ballotpedia.org"] = "https://ballotpedia.org/wiki/skins/Ballotpedia/images/bp-logo.svg"
org_logos["nytimes.com"] = "https://a1.nyt.com/assets/homepage/20161012-091952/images/foundation/logos/nyt-logo-379x64.png"

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
            return 1
        return 0

class NewsArticleItem(cm.ParticipationItem):
    def get_description(self):
        return self.participation_project.manualnewscurationproject.first_paragraph[:300]+"..."

    def set_display_image(self):
        for org in org_logos:
            if org in self.participation_project.url:
                self.display_image_url = org_logos[org]
                return
        self.display_image_url = 'manual_news_article_curation/img/default.png'

from __future__ import unicode_literals
from django.contrib.gis.db import models

from core import models as cm

org_logos = dict()
org_logos["ballotpedia.org"] = "manual_news_article_curation/img/bp-logo.svg"
org_logos["challenge.gov"] = "manual_news_article_curation/img/challenge_full_logo.png"

class ManualNewsCurationProject(cm.ParticipationProject):
    url = models.URLField(blank=False)
    screenshot_filename = models.FilePathField(max_length=500, blank=True)
    first_paragraph = models.TextField(blank=False)
    tags = models.ManyToManyField(cm.Tag)

    def update_items(self):
        existing_query_set = NewsArticleItem.objects.filter(participation_project=self, is_active=True)
        num_existing_items = existing_query_set.update(name=self.name)
        if num_existing_items == 0:
            item = NewsArticleItem()
            item.name = self.name
            item.participation_project = self
            item.save()
        else:
            for item in existing_query_set:
                item.set_relevant_tags()

class NewsArticleItem(cm.ParticipationItem):
    def get_inline_display(self):
        return self.participation_project.manualnewscurationproject.first_paragraph[:300]+"..."

    def set_display_image(self):
        if not self.participation_project.screenshot_filename is None:
            self.display_image_file = self.participation_project.screenshot_filename
            return
        for org in org_logos:
            if org in self.participation_project.url:
                self.display_image_file = org_logos[org]
                return
        self.display_image_file = 'manual_news_article_curation/img/default.png'

    def set_relevant_tags(self):
        self.tags.set([x.id for x in self.participation_project.get_inherited_instance().tags.all()])

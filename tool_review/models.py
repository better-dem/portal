from __future__ import unicode_literals

from django.db import models
from core import models as cm

class ToolReviewProject(cm.ParticipationProject):
    # name <- tool's name
    url = models.URLField(blank=False)
    screenshot_filename = models.FilePathField(max_length=500, blank=True)
    summary = models.TextField(blank=False)
    review_video = models.URLField(blank=True)
    review_blog_post = models.URLField(blank=True)
    tags = models.ManyToManyField(cm.Tag)
    
    def update_items(self):
        if ToolReviewItem.objects.filter(participation_project=self).count()==0:
            item = ToolReviewItem()
            item.name = self.name
            item.participation_project = self
            item.save()
            return set([item.id])
        return set()

class ToolReviewItem(cm.ParticipationItem):
    def get_description(self):
        return "Tool review for "+self.name

    def set_relevant_tags(self):
        self.tags.add(*self.participation_project.tags.all())

    def set_display_image(self):
        return None



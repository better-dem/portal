from __future__ import unicode_literals

from django.db import models
from core import models as cm

TOOL_CATEGORIES = (("OD", "Open Data"), ("ED", "Educational Material"), ("PA", "Policy Analysis"), ("CL", "Collaborative Problem-Solving"), ("UN", "Unclassified"))
PROJECT_CATEGORIES = (("GV","Government Project"), ("OS", "Open source project"), ("CO", "Commercial Product"), ("UN", "Unclassified"), ("NC", "Nonprofit Closed Source"))

class ToolReviewProject(cm.ParticipationProject):
    # name <- tool's name
    url = models.URLField()
    screenshot_filename = models.FilePathField(max_length=500, blank=True)
    summary = models.TextField()
    youtube_video_id = models.CharField(max_length=100, blank=True)
    review_blog_post = models.URLField(blank=True)
    tags = models.ManyToManyField(cm.Tag)
    tool_category = models.CharField(max_length=2, choices=TOOL_CATEGORIES, default="UN")
    project_category = models.CharField(max_length=2, choices=PROJECT_CATEGORIES, default="UN")
    
    def update_items(self):
        if ToolReviewItem.objects.filter(participation_project=self, is_active=True).count()==0:
            item = ToolReviewItem()
            item.name = self.name
            item.participation_project = self
            item.save()
            return set([item.id])
        return set()

class ToolReviewItem(cm.ParticipationItem):
    def get_inline_display(self):
        return self.participation_project.get_inherited_instance().summary

    def set_relevant_tags(self):
        self.tags.add(*self.participation_project.tags.all())

    def set_display_image(self):
        if not self.participation_project.screenshot_filename is None:
            self.display_image_file = self.participation_project.screenshot_filename
        # else:
        #     self.display_image_file = "tool_review/img/default.png"



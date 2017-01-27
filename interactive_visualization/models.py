from __future__ import unicode_literals

from django.db import models
from core import models as cm

class InteractiveVisualizationProject(cm.ParticipationProject):
    instructions_note = models.TextField()

    methodology_url = models.URLField()
    methodology_note = models.TextField()

    csv_data = models.TextField()

    # a switch variable is useful if the visualization is supposed to let 
    # viewers compare mutex scenarios (pie variables are similar, but not mutex)
    switch_variable = models.CharField(max_length=50, blank=True, null=True)
    switch_title = models.CharField(max_length=50, blank=True, null=True)
    switch_note = models.TextField(blank=True, null=True)

    # add charts to the visualization
    pie1_variable = models.CharField(max_length=50, blank=True, null=True)
    pie1_title = models.CharField(max_length=50, blank=True, null=True)

    bar1_variable = models.CharField(max_length=50, blank=True, null=True)
    bar1_title = models.CharField(max_length=50, blank=True, null=True)
    bar1_x_label = models.CharField(max_length=50, blank=True, null=True)
    bar1_y_label = models.CharField(max_length=50, blank=True, null=True)

    pie2_variable = models.CharField(max_length=50, blank=True, null=True)
    pie2_title = models.CharField(max_length=50, blank=True, null=True)

    bar2_variable = models.CharField(max_length=50, blank=True, null=True)
    bar2_title = models.CharField(max_length=50, blank=True, null=True)
    bar2_x_label = models.CharField(max_length=50, blank=True, null=True)
    bar2_y_label = models.CharField(max_length=50, blank=True, null=True)

    def update_items(self):
        if InteractiveVisualizationItem.objects.filter(participation_project=self, is_active=True).count()==0:
            item = InteractiveVisualizationItem()
            item.name = self.name
            item.participation_project = self
            item.save()
            return set([item.id])
        return set()

class InteractiveVisualizationItem(cm.ParticipationItem):
    def get_inline_display(self):
        return "interactive visualization " + str(self.id)

    def set_relevant_tags(self):
        self.tags.add(*self.participation_project.tags.all())

    def set_display_image(self):
        self.display_image_file = "interactive_visualization/img/default.png"

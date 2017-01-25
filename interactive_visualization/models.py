from __future__ import unicode_literals

from django.db import models
from core import models as cm

class InteractiveVisualizationProject(cm.ParticipationProject):

    def update_items(self):
        pass

class InteractiveVisualizationItem(cm.ParticipationItem):
    def get_inline_display(self):
        return "interactive visualization " + str(self.id)

    def set_relevant_tags(self):
        self.tags.add(*self.participation_project.tags.all())

    def set_display_image(self):
        self.display_image_file = "interactive_visualization/img/default.png"

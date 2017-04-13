from __future__ import unicode_literals

from django.db import models
from core import models as cm

CHAMBERS = (("UP", "upper"), ("LO", "lower"))

class LegislatorsProject(cm.ParticipationProject):
    open_states_leg_id = models.CharField(max_length=100)
    open_states_active = models.BooleanField()
    open_states_state = models.CharField(max_length=50)
    photo_url = models.URLField()
    webpage_url = models.URLField()
    chamber = models.CharField(max_length=2, choices=CHAMBERS, blank=True, null=True)
    district = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    
    def update_items(self):
        if LegislatorsItem.objects.filter(participation_project=self, is_active=True).count()==0:
            item = LegislatorsItem()
            item.name = self.name
            item.participation_project = self
            item.save()
            return set([item.id])
        return set()

class LegislatorsItem(cm.ParticipationItem):
    def get_inline_display(self):
        return self.participation_project.get_inherited_instance().summary

    def set_relevant_tags(self):
        self.tags.add(*self.participation_project.tags.all())

    def set_display_image(self):
        self.display_image_file = "legislators/img/default.png"


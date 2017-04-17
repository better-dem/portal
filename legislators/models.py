from __future__ import unicode_literals

from django.db import models
from core import models as cm

class LegislatorsProject(cm.ParticipationProject):
    open_states_leg_id = models.CharField(max_length=100)
    open_states_active = models.BooleanField()
    open_states_state = models.CharField(max_length=50)
    photo_url = models.URLField(null=True, blank=True)
    webpage_url = models.URLField(null=True, blank=True)
    chamber = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    tags = models.ManyToManyField(cm.Tag)
    
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
        return self.participation_project.get_inherited_instance().name

    def set_relevant_tags(self):
        self.tags.add(*self.participation_project.tags.all())

    def set_display_image(self):
        self.display_image_file = "legislators/img/default.png"

class BillsProject(cm.ParticipationProject):
    open_states_bill_id = models.CharField(max_length=100)
    bill_id = models.CharField(max_length=100)
    tags = models.ManyToManyField(cm.Tag)
    first_action_date = models.DateField(null=True, blank=True)
    last_action_date = models.DateField(null=True, blank=True)
    passed_upper_date = models.DateField(null=True, blank=True)
    passed_lower_date = models.DateField(null=True, blank=True)
    signed_date = models.DateField(null=True, blank=True)

class BillsItem(cm.ParticipationItem):
    def get_inline_display(self):
        return self.participation_project.get_inherited_instance().name

    def set_relevant_tags(self):
        self.tags.add(*self.participation_project.tags.all())

    def set_display_image(self):
        self.display_image_file = "legislators/img/default.png"


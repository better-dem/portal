from __future__ import unicode_literals

from django.db import models
from core import models as cm
from core import tasks as ct

DEFAULT_LEG_IMG = "legislators/img/default.png"

class LegislatorsProject(cm.ParticipationProject):
    open_states_leg_id = models.CharField(max_length=100, db_index=True)
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
        existing_query_set = LegislatorsItem.objects.filter(participation_project=self, is_active=True)
        num_existing_items = existing_query_set.update(name=self.name)
        if num_existing_items == 0:
            item = LegislatorsItem()
            item.name = self.name
            item.participation_project = self
            item.save()
        else:
            for item in existing_query_set:
                item.set_relevant_tags()
                if item.display_image_file == DEFAULT_LEG_IMG:
                    item.set_display_image()

class LegislatorsItem(cm.ParticipationItem):
    def get_inline_display(self):
        return self.participation_project.get_inherited_instance().name

    def set_relevant_tags(self):
        self.tags.set([x.id for x in self.participation_project.get_inherited_instance().tags.all()])

    def set_display_image(self):
        # set a temporary image
        if self.display_image_file is None or self.display_image_file == "":
            self.display_image_file = DEFAULT_LEG_IMG
        # scrape the provided image
        img_url = self.participation_project.get_inherited_instance().photo_url
        if not img_url is None:
            ct.scrape_image_and_set_field.delay(img_url, None, self.id, "display_image_file")

class BillsProject(cm.ParticipationProject):
    open_states_bill_id = models.CharField(max_length=100, db_index=True)
    bill_id = models.CharField(max_length=100)
    tags = models.ManyToManyField(cm.Tag)
    first_action_date = models.DateField(null=True, blank=True)
    last_action_date = models.DateField(null=True, blank=True)
    passed_upper_date = models.DateField(null=True, blank=True)
    passed_lower_date = models.DateField(null=True, blank=True)
    signed_date = models.DateField(null=True, blank=True)
    documents = models.ManyToManyField(cm.ReferenceDocument)

    def update_items(self):
        existing_query_set = BillsItem.objects.filter(participation_project=self, is_active=True)
        num_existing_items = existing_query_set.update(name=self.name, last_action_date=self.last_action_date)
        if num_existing_items == 0:
            item = BillsItem()
            item.name = self.name
            item.participation_project = self
            item.last_action_date = self.last_action_date
            item.save()
        else:
            for item in existing_query_set:
                item.set_relevant_tags()

class BillsItem(cm.ParticipationItem):
    last_action_date = models.DateField(null=True, blank=True)
    class Meta:
        get_latest_by="last_action_date"

    def get_inline_display(self):
        return self.participation_project.get_inherited_instance().name

    def set_relevant_tags(self):
        self.tags.set([x.id for x in self.participation_project.get_inherited_instance().tags.all()])

    def set_display_image(self):
        self.display_image_file = "legislators/img/bills_default.png"


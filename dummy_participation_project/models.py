from __future__ import unicode_literals
from django.contrib.gis.db import models

from core import models as cm

class DummyProject(cm.ParticipationProject):

    def update_items(self):
        if DummyItem.objects.filter(participation_project=self).count() == 0:
            item = DummyItem()
            item.name = self.name
            item.participation_project = self
            item.save()
            return 1
        return 0

class DummyItem(cm.ParticipationItem):
    def get_description(self):
        return self.name + "DUMMY participation item"



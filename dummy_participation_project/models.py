from __future__ import unicode_literals
from django.db import models

from core import models as cm

class DummyProject(cm.ParticipationProject):
    pass

class DummyItem(cm.ParticipationItem):
    def get_description(self):
        return self.name + "DUMMY participation item"



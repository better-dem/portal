from __future__ import unicode_literals

from django.db import models

import core.models as cm
from core.models import ParticipationProject, ParticipationItem

# register DummyItem with core app
cm.participation_item_subclass_tests.append(lambda x: x.dummyitem)


class DummyProject(cm.ParticipationProject):
    pass


class DummyItem(cm.ParticipationItem):
    def get_description(self):
        return self.name + "DUMMY participation item"



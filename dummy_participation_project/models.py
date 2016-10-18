from __future__ import unicode_literals
from django.db import models

from core import models as cm
from core import ParticipationApp as cp

# register DummyItem with core app
cp.register(cp.ParticipationApp(lambda x: x.dummyitem))


class DummyProject(cm.ParticipationProject):
    pass

class DummyItem(cm.ParticipationItem):
    def get_description(self):
        return self.name + "DUMMY participation item"



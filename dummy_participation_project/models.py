from __future__ import unicode_literals
from django.db import models

from core import models as cm
from core import ParticipationApp as cp
from . import views as views_module

class DummyProject(cm.ParticipationProject):
    pass

class DummyItem(cm.ParticipationItem):
    def get_description(self):
        return self.name + "DUMMY participation item"


# register NewsArticleItem with core app
cp.register(cp.ParticipationApp("DummyApp", DummyProject, lambda x: x.dummyitem, views_module))


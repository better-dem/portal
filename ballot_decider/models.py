from __future__ import unicode_literals

from django.db import models
from core import models as cm

class BallotDeciderProject(cm.ParticipationProject):
    ballot_text = models.TextField()
    election_date = models.DateField()
    election_website = models.URLField()

    # display a feed of related quizzes and tools in the "back to basics" section of the ballot decider
    basics = models.ManyToManyField(cm.ParticipationItem)
    points_of_view = models.ManyToManyField('PointOfView')

    tags = models.ManyToManyField(cm.Tag)

    def update_items(self):
        if BallotDeciderItem.objects.filter(participation_project=self, is_active=True).count()==0:
            item = BallotDeciderItem()
            item.name = self.name
            item.participation_project = self
            item.save()
            return set([item.id])
        return set()

class PointOfView(models.Model):
    quote = models.TextField()
    citation_url = models.URLField()
    favorability = models.FloatField() # restrict to be between 0 and 1 in the form?

class BallotDeciderItem(cm.ParticipationItem):
    def get_inline_display(self):
        return "Ballot decider for " + str(self.name)

    def set_relevant_tags(self):
        self.tags.add(*self.participation_project.tags.all())

    def set_display_image(self):
        self.display_image_file = "single_quiz/img/default.png"

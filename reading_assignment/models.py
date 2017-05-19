from __future__ import unicode_literals
from django.contrib.gis.db import models
from core import models as cm
import sys

class ReadingAssignmentProject(cm.ParticipationProject):
    tags = models.ManyToManyField(cm.Tag)

    def update_items(self):
        if ReadingAssignmentItem.objects.filter(participation_project=self).count() == 0:
            item = ReadingAssignmentItem()
            item.name = self.name
            item.participation_project = self
            item.save()
            return set([item.id])
        return set()


class ReadingAssignmentItem(cm.ParticipationItem):
    def get_inline_display(self):
        ans = "Land use planning project"
        if self.tags.all().count() > 0:
            ans += " for "+self.tags.all()[0].get_name()
        return ans

    def set_display_image(self):
        self.display_image_file = 'reading_assignment/img/default.png'

    def set_relevant_tags(self):
        self.tags.set([x.id for x in self.participation_project.get_inherited_instance().tags.all()])

class OrderedAssignmentItem(models.Model):
    number = models.PositiveIntegerField()
    text_question = models.ForeignKey(TextQuestion)
    participation_item = models.ForeignKey(cm.ParticipationItem)

class Submission(models.Model):
    user_profile = models.ForeignKey(cm.UserProfile, on_delete = models.CASCADE)
    participation_item = models.ForeignKey(ReadingAssignmentItem, on_delete = models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True)

class TextQuestion(models.Model):
    question_text = models.TextField()

class TextQuestionResponse(models.Model):
    question = models.ForeignKey(TextQuestion)
    response = models.TextField()
    submission = models.ForeignKey(Submission)
    

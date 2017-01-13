from __future__ import unicode_literals

from django.db import models
from core import models as cm

class SingleQuizProject(cm.ParticipationProject):
    question_text = models.CharField(max_length=500)
    option1 = models.CharField(max_length = 100)
    option2 = models.CharField(max_length = 100)
    option3 = models.CharField(max_length = 100, blank=True, null=True)
    option4 = models.CharField(max_length = 100, blank=True, null=True)
    option5 = models.CharField(max_length = 100, blank=True, null=True)
    correct_answer_index = models.IntegerField() # 1-5 (not 0-4)
    citation_url = models.URLField()
    explanation = models.TextField()
    tags = models.ManyToManyField(cm.Tag)

    def update_items(self):
        if SingleQuizItem.objects.filter(participation_project=self, is_active=True).count()==0:
            item = SingleQuizItem()
            item.name = self.name
            item.participation_project = self
            item.save()
            return set([item.id])
        return set()


class SingleQuizItem(cm.ParticipationItem):
    def get_inline_display(self):
        return "single quiz " + str(self.id)

    def set_relevant_tags(self):
        self.tags.add(*self.participation_project.tags.all())

    def set_display_image(self):
        self.display_image_file = "single_quiz/img/default.png"


class SingleQuizResponse(models.Model):
    user_profile = models.ForeignKey(cm.UserProfile, on_delete = models.CASCADE)
    participation_item = models.ForeignKey(SingleQuizItem, on_delete = models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True)
    answer_index = models.IntegerField()

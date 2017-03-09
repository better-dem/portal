from __future__ import unicode_literals

from django.db import models
import core.models as cm

class BeatTheBullshitProject(cm.ParticipationProject):
    topic_overview = models.TextField()
    tags = models.ManyToManyField(cm.Tag)

    def update_items(self):
        if BeatTheBullshitItem.objects.filter(participation_project=self, is_active=True).count()==0:
            item = BeatTheBullshitItem()
            item.name = self.name
            item.participation_project = self
            item.save()
            return set([item.id])
        return set()

class BeatTheBullshitItem(cm.ParticipationItem):
    def get_inline_display(self):
        return str(self.name)

    def set_relevant_tags(self):
        self.tags.add(*self.participation_project.tags.all())

    def set_display_image(self):
        self.display_image_file = "single_quiz/img/default.png"

class Quote(models.Model):
    quote_string = models.TextField()
    speaker_name = models.CharField(max_length = 500)
    reference = models.URLField()
    screenshot_filename = models.FilePathField(max_length=500, blank=True)
    project = models.ForeignKey('BeatTheBullshitProject', on_delete=models.CASCADE)

class Fallacy(models.Model):
    name = models.CharField(max_length = 500)
    description = models.TextField()
    example_context = models.TextField() # the context statement to which the example is a reply
    example = models.TextField() # an example phrase which commits this fallacy
    improvement = models.TextField() # an alternative way of phrasing the example

    def __unicode__(self):
        return self.name
    
class QuoteFallacyAssociation(models.Model):
    quote = models.ForeignKey('Quote', on_delete=models.CASCADE)
    fallacy = models.ForeignKey('Fallacy', on_delete=models.CASCADE)
    explanation = models.TextField()
    improvement = models.TextField() # an alternative way of phrasing the quote to avoid the fallacy
    
class QuoteFallacyQuizItemResponse(models.Model):
    user_profile = models.ForeignKey(cm.UserProfile, on_delete = models.CASCADE)
    participation_item = models.ForeignKey(BeatTheBullshitItem, on_delete = models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True)
    choice = models.ForeignKey(Fallacy, on_delete = models.SET_NULL, null=True)


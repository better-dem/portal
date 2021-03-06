from __future__ import unicode_literals

from django.db import models
import core.models as cm

class BeatTheBullshitProject(cm.ParticipationProject):
    topic_overview = models.TextField()
    bullet_1 = models.TextField(blank=True, null=True)
    bullet_2 = models.TextField(blank=True, null=True)
    bullet_3 = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField(cm.Tag)

    def update_items(self):
        existing_query_set = BeatTheBullshitItem.objects.filter(participation_project=self, is_active=True)
        num_existing_items = existing_query_set.update(name=self.name)
        if num_existing_items == 0:
            item = BeatTheBullshitItem()
            item.name = self.name
            item.participation_project = self
            item.save()
        else:
            for item in existing_query_set:
                item.set_relevant_tags()

class BeatTheBullshitItem(cm.ParticipationItem):
    def get_inline_display(self):
        return str(self.name)

    def set_relevant_tags(self):
        self.tags.set([x.id for x in self.participation_project.get_inherited_instance().tags.all()])

    def set_display_image(self):
        self.display_image_file = "beat_the_bullshit/img/human_brain.jpg"

class Quote(models.Model):
    quote_string = models.TextField()
    speaker_name = models.CharField(max_length = 500)
    reference = models.URLField()
    screenshot_filename = models.FilePathField(max_length=500, blank=True)
    youtube_video_id = models.CharField(max_length=100, blank=True)
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
    is_correct = models.BooleanField()

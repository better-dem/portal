from __future__ import unicode_literals
from django.contrib.gis.db import models
from core import models as cm
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
import sys

class LandUseProject(cm.ParticipationProject):
    feedback_goals = models.ManyToManyField('FeedbackGoal')
    polygon = models.PolygonField(geography = True)

    def get_questions(self):
        ans = []
        for goal in self.feedback_goals.all():
            for question in Question.objects.filter(feedback_goal = goal):
                ans.append(question)
        return ans

    def update_items(self):
        if LandUseParticipationItem.objects.filter(participation_project=self).count() == 0:
            item = LandUseParticipationItem()
            item.name = self.name
            item.participation_project = self
            item.save()
            return set([item.id])
        return set()

    def polygon_for_google(self):
        # swap lat/lon indices (Google does lat,lon, which nobody else does)
        # remove the last item, postGIS requires a closed ring, google doesn't
        coords = [c for c in self.polygon[0]]
        # eliminate the last point, which closes the ring
        coords = coords[:-1]
        # swap indices, turn into an array, not tuple
        coords = [[c[1], c[0]] for c in coords]
        return coords
        

class LandUseParticipationItem(cm.ParticipationItem):
    def get_description(self):
        ans = "Land use planning project"
        if self.tags.all().count() > 0:
            ans += " for "+self.tags.all()[0].get_name()
        return ans

    def set_display_image(self):
        self.display_image_file = 'land_use_planning/img/default.png'

    def set_relevant_tags(self):
        pnt = GEOSGeometry(self.participation_project.polygon).centroid
        search_radius_m = 50000  # meters?
        nearest_cities = cm.GeoTag.objects.filter(feature_type=cm.GeoTag.CITY).filter(point__distance_lte=(pnt, D(m=search_radius_m))).annotate(distance=Distance('point', pnt)).order_by('distance')[:5]
        sys.stderr.write("cities nearest to this project: "+str([x.get_name() for x in nearest_cities])+"\n")
        sys.stderr.flush()
        self.tags.add(*nearest_cities[:1])


class ItemResponse(models.Model):
    user_profile = models.ForeignKey(cm.UserProfile, on_delete = models.CASCADE)
    participation_item = models.ForeignKey(LandUseParticipationItem, on_delete = models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True)

class FeedbackGoal(models.Model):
    name = models.CharField(max_length = 100)
    description = models.CharField(max_length = 200)

class Question(models.Model):
    feedback_goal = models.ForeignKey('FeedbackGoal', on_delete=models.CASCADE)
    question_text = models.CharField(max_length = 200)

#Text Multi Choice Question
class TMCQ(Question):
    option1 = models.CharField(max_length = 100)
    option2 = models.CharField(max_length = 100)
    option3 = models.CharField(max_length = 100)
    option4 = models.CharField(max_length = 100)
    option5 = models.CharField(max_length = 100)


class QuestionResponse(models.Model):
    item_response = models.ForeignKey(
            ItemResponse,
            on_delete = models.CASCADE,
        )
    question = models.ForeignKey(
            'Question',
            on_delete = models.CASCADE,
        )

class TMCQResponse(QuestionResponse):
    option_index = models.IntegerField()

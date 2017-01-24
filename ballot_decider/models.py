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

class POVToolResponse(models.Model):
    """
    This model captures a user submission of a set of weighted points of view.
    """
    user_profile = models.ForeignKey(cm.UserProfile, on_delete = models.CASCADE)
    participation_item = models.ForeignKey(BallotDeciderItem, on_delete = models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True)

    def generate_decision(self):
        item_responses = self.povitemresponse_set.all()
        scored_response_strings = {k.point_of_view.quote: k.point_of_view.favorability*k.score for k in item_responses}
        pros = [k in item_responses if k.point_of_view.favorability > 0]
        cons = [k for k in item_responses if k.point_of_view.favorability < 0]
        sorted_pros = sorted(pros, key=lambda x: abs(scored_response_strings[x]), reverse=True)
        sorted_cons = max(cons, key=lambda x: abs(scored_response_strings[x]), reverse=True)
        if len(scored_response_strings) == 0:
            final_decision = 0
        else: 
            final_decision = 1.0 * sum(scored_response_strings) / len(scored_response_strings)

        explanation = ""
        if final_decision > 0:
            concessions = [k for k in sorted_cons if not scored_response_strings[k] == 0]
            if len(concessions) > 0:
                explanation += "Although I agree that " + concessions[0] + ", "
            main_argument = sorted_pros[0]
            if abs(scored_response_strings[main_argument]) > \
               abs(scored_response_strings[concessions[0]]):
                explanation += "I decided to vote yes because "+main_argument+"."

        elif final_decision < 0:
            concessions = [k for k in sorted_pros if not scored_response_strings[k] == 0]
            if len(concessions) > 0:
                explanation += "Although I agree that " + concessions[0] + ", "
            main_argument = sorted_cons[0]
            if abs(scored_response_strings[main_argument]) > \
               abs(scored_response_strings[concessions[0]]):
                explanation += "I decided to vote no because "+main_argument+"."

        else:
            if len([k for k in scored_response_strings if not scored_response_strings[k] == 0]) == 0:
                explanation = "I don't care at all about this issue, so I'll abstain from voting."
            else:
                explanation = "I find that the pros and cons completely cancel each other out, so I'll abstain from voting."

        return {"decision": final_decision, "explanation": explanation}
        

class POVItemResponse(models.Model):
    point_of_view = models.ForeignKey(PointOfView)
    score = models.FloatField()

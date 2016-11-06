from __future__ import unicode_literals
from django.db import models
from core import models as cm
import sys
import random

fake_first_names = ["John", "Alfonso", "Meg", "David", "Akshay", "Erika", "Kurt", "Casey", "Terry", "Monique", "Carmen", "Marco"]
fake_last_names = ["Thatcher", "McGregor", "Testerman", "Hodges", "Black", "Ericson", "Chen", "Joseph", "Lester", "Lopez", "Jackson", "Hollande"]
fake_budgets = [[i*pow(10,j) for i in range(1,10)] for j in range(4,7)]

def gen_random_name(different_than=None):
    n = random.choice(fake_first_names)+" "+random.choice(fake_last_names)
    while not different_than == n:
        n = random.choice(fake_first_names)+" "+random.choice(fake_last_names)
    return n

def gen_random_budget(different_than=None):
    """
    generate a number that is sufficiently different than and plausibly close to
    the actual budget
    """
    def ratio (x,y):
        if x>y:
            return x/y
        return y/x

    n = random.choice(fake_budgets)    
    while ratio(n, different_than)<1.3 or ratio(n, different_than)>100:
        n = random.choice(fake_budgets)
    return n



class CityBudgetingProject(cm.ParticipationProject):
    city = models.ForeignKey(cm.GeoTag, on_delete = models.CASCADE)
    fiscal_year_end_date = models.DateField()
    total_expected_revenue = models.PositiveIntegerField() # in thousands of dollars
    total_expected_expenditure = models.PositiveIntegerField() # in thousands of dollars
    mayor_name = models.CharField(max_length=100)
    council_members = models.TextField() # comma separated names of council memebers
    budget_url = models.URLField(blank=False)
    
    def update_items(self):
        # generate basic quiz
        if CityBudgetQuiz.objects.filter(participation_project=self).count() == 0:
            item = CityBudgetQuiz()
            item.name = self.name
            item.participation_project = self
            item.save()

            q1 = TMCQ()
            q1.item = item
            q1.question_text = "Who is "+self.city.name+"'s Mayor?"
            for i in range(5):
                q1.__dict__["option"+str(i+1)] = gen_random_name(self.mayor_name)
            c = random.randrange(0,5)
            q1.correct_answer_index = c
            q1.__dict__["option"+str(c+1)] = self.mayor_name
            q1.save()

            q2 = TMCQ()
            q2.item = item
            q2.question_text = "How much revenue does the "+self.city.name+" budget expect for the fiscal year ending in "+str(self.fiscal_year_end_date.strftime("%B %d, %Y"))+"?"

            for i in range(5):
                q2.__dict__["option"+str(i+1)] = gen_random_budget(self.total_expected_expenditure)
            c = random.randrange(0,5)
            q2.correct_answer_index = c
            q2.__dict__["option"+str(c+1)] = self.total_expected_revenue
            q2.save()

            return set([item.id])
        return set()

class CityBudgetQuiz(cm.ParticipationItem):
    def get_description(self):
        ans = "City budget quiz"
        if self.tags.all().count() > 0:
            ans += " for "+self.tags.all()[0].get_name()
        return ans

    def set_display_image(self):
        self.display_image_url = 'city_budgeting/img/default.png'

    def set_relevant_tags(self):
        self.tags.add(self.participation_project.city)


class QuizResponse(models.Model):
    user_profile = models.ForeignKey(cm.UserProfile, on_delete = models.CASCADE)
    participation_item = models.ForeignKey(CityBudgetQuiz, on_delete = models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True)

class Question(models.Model):
    item = models.ForeignKey(CityBudgetQuiz, on_delete=models.CASCADE)
    question_text = models.CharField(max_length = 200)

#Text Multi Choice Question
class TMCQ(Question):
    option1 = models.CharField(max_length = 100)
    option2 = models.CharField(max_length = 100)
    option3 = models.CharField(max_length = 100)
    option4 = models.CharField(max_length = 100)
    option5 = models.CharField(max_length = 100)
    correct_answer_index = models.IntegerField()

class QuestionResponse(models.Model):
    item_response = models.ForeignKey(
            QuizResponse,
            on_delete = models.CASCADE,
        )
    question = models.ForeignKey(
            'Question',
            on_delete = models.CASCADE,
        )

class TMCQResponse(QuestionResponse):
    option_index = models.IntegerField()


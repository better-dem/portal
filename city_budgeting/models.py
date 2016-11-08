from __future__ import unicode_literals
from django.db import models
from core import models as cm
import sys
import random

fake_first_names = ["John", "Alfonso", "Meg", "David", "Akshay", "Erika", "Kurt", "Casey", "Terry", "Monique", "Carmen", "Marco"]
fake_last_names = ["Thatcher", "McGregor", "Testerman", "Hodges", "Black", "Ericson", "Chen", "Joseph", "Lester", "Lopez", "Jackson", "Hollande"]
fake_budgets = []

for j in range(1,10):
    for i in range(1,100):
        fake_budgets.append(i*pow(10,j))

def gen_random_name(different_than=None):
    n = random.choice(fake_first_names)+" "+random.choice(fake_last_names)
    if isinstance(different_than, list):
        while n in different_than:
            n = random.choice(fake_first_names)+" "+random.choice(fake_last_names)
    elif isinstance(different_than, str):
        while different_than == n:
            n = random.choice(fake_first_names)+" "+random.choice(fake_last_names)
    return n

def gen_random_budget(different_than=None):
    """
    generate a number that is sufficiently different than and plausibly close to
    the actual budget
    """
    def ratio (x,y):
        if x>y:
            return 1.0*x/y
        return 1.0*y/x

    n = random.choice(fake_budgets)    
    while ratio(n, different_than)<1.3 or ratio(n, different_than)>100:
        n = random.choice(fake_budgets)
    return n
    
class Service(models.Model):
    city_budget = models.ForeignKey('CityBudgetingProject', on_delete=models.CASCADE)

    SERVICE_TYPES = (("FR", "Fire and Rescue"), ("PO", "Police"), ("SW", "Sewage and Storm Water"), ("LB", "Library"), ("PR", "Parks and Recreation"), ("CM", "Cemetery"), ("WA", "Water"), ("EG", "Electric and Gas"), ("GR", "Garbage and Recycling"), ("TR", "Transit"))
    service_type = models.CharField(max_length=2, choices=SERVICE_TYPES)

    SOURCE_CHOICES = (("PC", "Provided by City"), ("PP", "Provided by Private Companies"), ("PR", "Provided through Regional Partnership"), ("NP", "Other / Not Provided"))
    source = models.CharField(max_length=2, choices=SOURCE_CHOICES, default="PC")
    expected_expenditure = models.PositiveIntegerField(blank=True, null=True)



class CityBudgetingProject(cm.ParticipationProject):
    city = models.ForeignKey(cm.GeoTag, on_delete = models.CASCADE)
    fiscal_year_end_date = models.DateField()
    total_expected_revenue = models.PositiveIntegerField() # in dollars
    total_expected_expenditure = models.PositiveIntegerField() # in dollars
    mayor_name = models.CharField(max_length=100)
    council_members = models.TextField() # comma separated names of council memebers
    budget_url = models.URLField(blank=False)
    
    def update_items(self):
        # generate basic quiz
        if CityBudgetQuiz.objects.filter(participation_project=self).count() == 0:
            sys.stderr.write("creating a new quiz\n")
            item = CityBudgetQuiz()
            item.name = self.name
            item.participation_project = self
            item.save()

            q1 = TMCQ()
            q1.item = item
            q1.question_text = "Who is "+self.city.name+"'s Mayor?"
            for i in range(5):
                q1.__dict__["option"+str(i+1)] = gen_random_name(self.mayor_name)
            c = random.randrange(1,6)
            q1.correct_answer_index = c
            q1.__dict__["option"+str(c)] = self.mayor_name
            q1.save()

            q2 = TMCQ()
            q2.item = item
            q2.question_text = "How much revenue does the "+self.city.name+" budget expect for the fiscal year ending in "+str(self.fiscal_year_end_date.strftime("%B %d, %Y"))+"?"

            for i in range(5):
                q2.__dict__["option"+str(i+1)] = gen_random_budget(self.total_expected_expenditure)
            c = random.randrange(1,6)
            q2.correct_answer_index = c
            q2.__dict__["option"+str(c)] = self.total_expected_revenue
            q2.save()

            q3 = TMCQ()
            q3.item = item
            q3.question_text = "Which of these people is NOT on "+self.city.name+"'s city council?"
            city_council_members = [x.strip() for x in self.council_members.split(',')]
            for i in range(5):
                q3.__dict__["option"+str(i+1)] = city_council_members[(100-i)%len(city_council_members)]
            c = random.randrange(1,6)
            q3.correct_answer_index = c
            q3.__dict__["option"+str(c)] = gen_random_name(city_council_members)
            q3.save()

            # "most expensive service"
            expensive_services = Service.objects.filter(city_budget=self).filter(expected_expenditure__isnull=False).order_by("-expected_expenditure")[:5]
            if len(expensive_services) > 4:
                q = TMCQ()
                q.item = item
                q.question_text = "Which of these services is most expensive this year?"
                shuff = list(expensive_services)
                random.shuffle(shuff)
                q.correct_answer_index = shuff.index(expensive_services[0])+1
                for i in range(5):
                    st = shuff[i]
                    st_str = [t[1] for t in Service.SERVICE_TYPES if t[0]==st.service_type][0]
                    q.__dict__["option"+str(i+1)] = st_str
                c = random.randrange(1,6)
                q.save()

            services_directly_provided = Service.objects.filter(city_budget=self).filter(source="PC").distinct()
            services_privately_provided = Service.objects.filter(city_budget=self).filter(source="PP").distinct()
            services_not_provided = Service.objects.filter(city_budget=self).filter(source="NP").distinct()
            services_provided_through_partnership = Service.objects.filter(city_budget=self).filter(source="PR").distinct()

            # how is a service provided?
            if services_directly_provided.count()>=4 and services_provided_through_partnership.count()>0:
                q = TMCQ()
                q.item = item
                q.question_text = "Which of these services is provided not by the city directly, but through a regional partnership?"
                shuff = list(services_directly_provided[:4])
                random.shuffle(shuff)
                c = random.randrange(5)
                q.correct_answer_index = c+1
                shuff.insert(c, services_provided_through_partnership[0])
                for i in range(5):
                    st = shuff[i]
                    st_str = [t[1] for t in Service.SERVICE_TYPES if t[0]==st.service_type][0]
                    q.__dict__["option"+str(i+1)] = st_str
                q.save()

            elif services_directly_provided.count()>=4 and services_privately_provided.count()>0:
                q = TMCQ()
                q.item = item
                q.question_text = "Which of these services does the city contract out to a private company?"
                shuff = list(services_directly_provided[:4])
                random.shuffle(shuff)
                c = random.randrange(5)
                q.correct_answer_index = c+1
                shuff.insert(c, services_privately_provided[0])
                for i in range(5):
                    st = shuff[i]
                    st_str = [t[1] for t in Service.SERVICE_TYPES if t[0]==st.service_type][0]
                    q.__dict__["option"+str(i+1)] = st_str
                q.save()

            elif services_directly_provided.count()>=4 and services_not_provided.count()>0:
                q = TMCQ()
                q.item = item
                q.question_text = "Which of these services does the city not provide?"
                shuff = list(services_directly_provided[:4])
                random.shuffle(shuff)
                c = random.randrange(5)
                q.correct_answer_index = c+1
                shuff.insert(c, services_not_provided[0])
                for i in range(5):
                    st = shuff[i]
                    st_str = [t[1] for t in Service.SERVICE_TYPES if t[0]==st.service_type][0]
                    q.__dict__["option"+str(i+1)] = st_str
                q.save()

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


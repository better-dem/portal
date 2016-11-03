from django.test import TestCase, TransactionTestCase
from land_use_planning.models import LandUseProject, FeedbackGoal, Question, QuestionResponse, TMCQResponse
from django.test import Client
from .forms import CreateProjectForm, ItemResponseForm
from django.core.urlresolvers import reverse

class SurveyAppUnitTests(TestCase):
    def setup(self):
        pass
        
    def test_if_db_is_empty(self):
        num_projects =  LandUseProject.objects.all().count()
        self.assertEqual(num_projects, 0)



        

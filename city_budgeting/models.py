from __future__ import unicode_literals
from django.db import models
from core import models as cm
import sys
import random
import json

def validate_budget_json(obj):
    assert(len(obj.keys()) == 3)
    assert("revenues" in obj.keys())
    assert("funds" in obj.keys()) 
    assert("expenses" in obj.keys())
    # much more here

class CityBudgetingProject(cm.ParticipationProject):
    city = models.ForeignKey(cm.GeoTag, on_delete = models.CASCADE)
    fiscal_period_start = models.DateField()
    fiscal_period_end = models.DateField()
    budget_json = models.TextField() # contains a budget_json format
    budget_json_version = models.IntegerField(default=1)
    budget_url = models.URLField(blank=False)
    
    def update_items(self):
        if CityBudgetingItem.objects.filter(participation_project=self, is_active=True).count()==0:
            item = CityBudgetingItem()
            item.name = self.name
            item.participation_project = self
            item.save()
            return set([item.id])
        return set()

    def set_name(self):
        self.name = "City Budget Outreach Project for "+project.city.get_name()

class CityBudgetingItem(cm.ParticipationItem):
    """
    The budget transparency interactive widget page
    """
    def get_inline_display(self):
        ans = "Interactive budget explorer"
        if self.tags.all().count() > 0:
            ans += " for "+self.tags.all()[0].get_name()
        return ans

    def set_display_image(self):
        self.display_image_file = 'city_budgeting/img/default.png'

    def set_relevant_tags(self):
        self.tags.add(self.participation_project.city)



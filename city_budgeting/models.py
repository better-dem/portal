from __future__ import unicode_literals
from django.db import models
from core import models as cm
import sys
import random
import json
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

def validate_budget_json(json_string):
    obj = None
    try:
        obj = json.loads(json_string)
    except Exception as e:
        raise ValidationError(_("Error parsing json:%(error)s"), params={'error': str(e)})
    try:
        assert(len(obj.keys()) == 3)
        assert("revenues" in obj.keys())
        assert("funds" in obj.keys()) 
        assert("expenses" in obj.keys())
        # much more here
    except Exception as e:
        raise ValidationError(("The budget JSON string must contain exactly 3 keys at the top level: revenues, funds, and expenses",))

class CityBudgetingProject(cm.ParticipationProject):
    city = models.ForeignKey(cm.GeoTag, on_delete = models.CASCADE)
    fiscal_period_start = models.DateField()
    fiscal_period_end = models.DateField()
    # contains a string in budget_json format
    budget_json = models.TextField(validators=[validate_budget_json]) 
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



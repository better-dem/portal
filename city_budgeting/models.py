from __future__ import unicode_literals
from django.db import models
from core import models as cm
import sys
import random
import json
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import traceback
from collections import Counter

def validate_budget_json(json_string):
    def assert_schema(d, schema):
        """ Ensure d follows schema exactly. All keys are required. Schema is just for depth=1 """
        try:
            assert(len(d.keys()) == len(schema))
        except AssertionError:
                raise ValidationError(_("keys: %(key)s don't match requirements: %(req)s"), params={'key': unicode(d.keys()), 'req': unicode(schema.keys())})
            
        for k in schema.keys():
            try:
                assert(k in d.keys())
            except AssertionError:
                raise ValidationError(_("missing key: %(key)s. Required keys: %(req)s"), params={'key': unicode(k), 'req': unicode(schema.keys())})
            try:
                assert(isinstance(d[k], schema[k]))
            except AssertionError:
                raise ValidationError(_("%(key)s isn't a %(type)s"), params={'key': unicode(d[k]), 'type': unicode(schema[k])})

    def assert_close_enough(n1, n2):
        """ Ensure that the difference between two numbers is within acceptable limit, rounding / float arithmetic errors """
        try: 
            assert(abs(1.0*n1 - 1.0*n2) < 1E-8*(n1+n2))
        except AssertionError:
            raise ValidationError(_("%(n1)s is supposed to be equal to %(n2)s"), params={'n1': unicode(n1), 'n2': unicode(n2)})


    obj = None
    try:
        obj = json.loads(json_string)
    except Exception as e:
        raise ValidationError(_("Error parsing json:%(error)s"), params={'error': unicode(e)})
    try:
        assert_schema(obj, {"description": unicode, "revenues": dict, "funds": dict, "expenses": dict})

        r = obj["revenues"]
        assert_schema(r, {"description": unicode, "items": list})
        for i in r["items"]:
            assert_schema(i, {"id": int, "name": unicode, "category": unicode,"amount": float, "description": unicode, "target_fund":int})

        f = obj["funds"] 
        assert_schema(f, {"description": unicode, "items": list})
        for i in f["items"]:
            assert_schema(i, {"id": int, "name": unicode, "category": unicode, "description":unicode})

        e = obj["expenses"]
        assert_schema(e, {"description": unicode, "items": list})
        for i in e["items"]:
            assert_schema(i, {"id": int, "name": unicode, "category": unicode,"amount": float, "description": unicode, "origin_fund":int})
            
        # much more here
    except Exception as e:
        sys.stderr.write(traceback.format_exc())
        sys.stderr.flush()
        raise ValidationError(_("Json string doesn't follow budget json schema: %(error)s"), params={'error': str(e)})

class CityBudgetingProject(cm.ParticipationProject):
    city = models.ForeignKey(cm.GeoTag, on_delete = models.CASCADE)
    fiscal_period_start = models.DateField()
    fiscal_period_end = models.DateField()
    # contains a string in budget_json format
    budget_json = models.TextField(validators=[validate_budget_json]) 
    budget_json_version = models.IntegerField(default=1)
    budget_url = models.URLField(blank=False)
    
    def update_items(self):
        existing_query_set = CityBudgetingItem.objects.filter(participation_project=self, is_active=True)
        num_existing_items = existing_query_set.update(name=self.name)
        if num_existing_items == 0:
            item = CityBudgetingItem()
            item.name = self.name
            item.participation_project = self
            item.save()
        else:
            for item in existing_query_set:
                item.set_relevant_tags()

    def set_name(self):
        self.name = "City Budget Outreach Project for "+self.city.get_name()

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
        self.tags.set([self.participation_project.get_inherited_instance().city.id])



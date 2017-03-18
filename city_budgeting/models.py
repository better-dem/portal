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
        assert(len(d.keys()) == len(schema))
        for k in schema.keys():
            assert(k in d.keys())
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
        assert_schema(obj, {"revenues": dict, "funds": dict, "expenses": dict})

        r = obj["revenues"]
        assert_schema(r, {"checksum": float, "category_checksums": dict, "items": list})
        checksum = r["checksum"]
        categories = r["category_checksums"].keys()
        assert_schema(r["category_checksums"], {k: float for k in categories})
        assert_close_enough(sum(r["category_checksums"].values()), checksum)
        category_sums = Counter({c:0 for c in categories})
        for i in r["items"]:
            assert_schema(i, {"id": int, "name": unicode, "category": unicode,"amount": float, "description": unicode})
            assert(i["category"] in categories)
            category_sums.update({i["category"]: i["amount"]})
        for c in categories:
            assert_close_enough(category_sums[c], r["category_checksums"][c])

        f = obj["funds"] 
        assert_schema(f, {"checksum": float, "category_checksums": dict, "items": list})
        checksum = f["checksum"]
        categories = f["category_checksums"].keys()
        assert_schema(f["category_checksums"], {k: float for k in categories})
        assert_close_enough(sum(f["category_checksums"].values()), checksum)
        category_sums = Counter({c:0 for c in categories})
        for i in f["items"]:
            assert_schema(i, {"id": int, "name": unicode, "category": unicode,"starting_balance": float})
            assert(i["category"] in categories)
            category_sums.update({i["category"]: i["starting_balance"]})
        for c in categories:
            assert_close_enough(category_sums[c], f["category_checksums"][c])

        e = obj["expenses"]
        assert_schema(e, {"checksum": float, "category_checksums": dict, "items": list})
        checksum = e["checksum"]
        categories = e["category_checksums"].keys()
        assert_schema(e["category_checksums"], {k: float for k in categories})
        assert_close_enough(sum(e["category_checksums"].values()), checksum)
        category_sums = Counter({c:0 for c in categories})
        for i in e["items"]:
            assert_schema(i, {"id": int, "name": unicode, "category": unicode,"amount": float, "description": unicode})
            assert(i["category"] in categories)
            category_sums.update({i["category"]: i["amount"]})
        for c in categories:
            assert_close_enough(category_sums[c], e["category_checksums"][c])
            
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
        if CityBudgetingItem.objects.filter(participation_project=self, is_active=True).count()==0:
            item = CityBudgetingItem()
            item.name = self.name
            item.participation_project = self
            item.save()
            return set([item.id])
        return set()

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
        self.tags.add(self.participation_project.city)



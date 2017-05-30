from django import forms
from django.forms.widgets import Textarea, DateInput, NumberInput
from s3direct.widgets import S3DirectWidget
from core import forms as cf
import json
import sys
from widgets import forms as wf
from city_budgeting.models import validate_budget_json

EXAMPLE_JSON="""{"description": "This is an example budget JSON for the fictional city of Happyville.",
 "funds":
 {
     "description":"Happyville has two funds: the general fund and the youth sports fund.",
     "items": 
     [
 {"id":0, "name":"General Fund", "category":"General Government Operating Funds", "description":"The General Fund is the primary operating fund of the City. The General Fund is used to account for resources traditionally associated with government which are not required by law or by sound financial management practice to be accounted for in another fund."},
 {"id":1, "name":"Youth Sports Fund", "category":"Special Revenue Funds", "description": "This fund is to support youth sports programs in Happyville."}
     ]
 }, 
 "revenues": 
 {
     "description":"All of Happyville's revenue is collected by Tom the Taxman.",
     "items": 
     [
 {"id":0, "name":"Property Tax", "category": "Taxes", "amount":1500.0, "description":"", "target_fund":0}, 
 {"id":1, "name":"Sales Tax", "category": "Taxes", "amount":300.0, "description":"Happyville's sales tax rate is 3%", "target_fund":0}, 
 {"id":2, "name":"Selling Hotdogs", "category": "Fees for Services", "amount":200.0, "description":"", "target_fund":1}, 
 {"id":3, "name":"Business Licenses", "category": "Permits and Licenses", "amount": 8540.0, "description":"", "target_fund":0},
 {"id":4, "name":"Home Renovation Permits", "category": "Permits and Licenses", "amount": 230.0, "description":"", "target_fund":0}
     ]
 }, 
 "expenses":
 {
     "description":"Happyville is a well-oiled fiscal machine.",
     "items": 
     [
 {"id":0, "name":"Salaries and Wages", "category":"Salaries and Wages", "amount":100.0, "description":"", "origin_fund": 0},
 {"id":1, "name":"Benefits", "category":"Benefits", "amount":100.0, "description":"", "origin_fund": 0},
 {"id":2, "name":"Supplies", "category":"Supplies", "amount":300.0, "description":"", "origin_fund": 0},
 {"id":3, "name":"Other Services and Charges", "category":"Other Services and Charges", "amount":250.0, "description":"", "origin_fund": 0},
 {"id":4, "name":"Reserves", "category":"Reserves", "amount":800.0, "description":"", "origin_fund": 0},
 {"id":5, "name":"Supplies", "category":"Supplies", "amount":100.0, "description":"Purchased gloves for the baseball team", "origin_fund": 1},
 {"id":6, "name":"Salaries and Wages", "category":"Salaries and Wages", "amount":100.0, "description":"Paid Old Jim to mow the lawn", "origin_fund": 1}
     ]
 }
}"""

class CreateProjectForm(forms.Form):
    name = forms.CharField(label="Project Name")
    fiscal_period_start = forms.DateField(widget = wf.DatePickerJQueryWidget)
    fiscal_period_end = forms.DateField(widget = wf.DatePickerJQueryWidget)
    
    budget_description = forms.CharField()
    revenues_description = forms.CharField()
    funds_description = forms.CharField()
    expenses_description = forms.CharField()

    budget_excel_file = forms.URLField(widget=S3DirectWidget(dest="file_upload"))

    # budget_json = forms.CharField(widget=Textarea(attrs={'style':"width:100%;", 'rows': 20, 'cols':2}), validators=[validate_budget_json], initial=EXAMPLE_JSON)
    budget_url = forms.URLField()
    city = cf.tag_aac.get_new_form_field(required=False)



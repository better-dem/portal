# legislators/tasks.py
from django.db import transaction
import core.models as cm
import core.tasks as ct
from legislators.models import LegislatorsProject, LegislatorsItem, BillsProject, BillsItem

import argparse
import datetime
import sys
import pyopenstates
import zipfile
import os
import json
import tempfile
import shutil

pyopenstates.session.headers.update({"X-API-KEY":os.environ["OPENSTATES_KEY"]})

def get_task(task_name):
    function, state_name, openstates_state_abbrev = task_name.split("|")
    if function == "update_state":
        return lambda : update_state_recent(state_name, openstates_state_abbrev)
        # return lambda : update_state_bulk(state_name, openstates_state_abbrev)

def update_state_recent(state_name, openstates_state_abbrev):
    """
    Update state information using repeated hits to the openstates API.
    Does not use bulk data, which appears to be aggregiously outdated
    (Bulk data only goes through mid 2016 (as of May 9, 2017))
    """
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month
    one_year_ago = "{}-{}-01".format(current_year-1,str(current_month).zfill(2))
    six_months_ago = "{}-{}-01".format(current_year if current_month>6 else current_year-1, str(current_month - 6 if current_month>6 else current_month + 6).zfill(2))
    one_month_ago = "{}-{}-01".format(current_year if current_month>1 else current_year-1, str(current_month - 1 if current_month>1 else 12).zfill(2))

    num_new_legislators = 0
    num_updated_legislators = 0
    num_legislator_exceptions = 0
    num_new_bills = 0
    num_updated_bills = 0
    num_bill_exceptions = 0

    sys.stdout.write("Updating state legislators and bills: {}\n".format(state_name))
    try:
        state_geotag = cm.GeoTag.objects.get(feature_type="SP", name=state_name)


        all_legislators = pyopenstates.search_legislators(state=openstates_state_abbrev)
        for leg_json in all_legislators:
            result = update_legislator(leg_json, state_geotag)
            if result == "updated":
                num_updated_legislators += 1
            elif result == "new":
                num_new_legislators += 1

        sys.stdout.write("Number of legislators added: {}\n".format(num_new_legislators))
        sys.stdout.write("Number of legislators updated: {}\n".format(num_updated_legislators))
        sys.stdout.write("Number of exceptions updating a legislator: {}\n".format(num_legislator_exceptions))

        recently_updated_bills = None
        # try to get recent bills up to 1 year old. If the API thinks it's too big of a request, try shorter periods
        try:
            recently_updated_bills = pyopenstates.search_bills(state=openstates_state_abbrev, updated_since=one_year_ago, fields=["title", "id", "bill_id", "subjects", "versions", "action_dates"])
        except pyopenstates.APIError as e:
            sys.stderr.write("Handling openstates APIError: {}\n trying a more recent update period\n".format(unicode(e)))
            recently_updated_bills = pyopenstates.search_bills(state=openstates_state_abbrev, updated_since=six_months_ago, fields=["title", "id", "bill_id", "subjects", "versions", "action_dates"])
        except pyopenstates.APIError as e:
            sys.stderr.write("Handling openstates APIError: {}\n trying a more recent update period\n".format(unicode(e)))
            recently_updated_bills = pyopenstates.search_bills(state=openstates_state_abbrev, updated_since=one_month_ago, fields=["title", "id", "bill_id", "subjects", "versions", "action_dates"])

        sys.stderr.write("Number of recently-updated bills: {}\n".format(len(recently_updated_bills)))

        for bill_json in recently_updated_bills:
            result = update_bill(bill_json, state_geotag)
            if result == "updated":
                num_updated_bills += 1
                if num_updated_bills % 100 == 0:
                    sys.stderr.write("Updating bill #{}\n".format(num_updated_bills))
            elif result == "new":
                num_new_bills += 1
                if num_new_bills % 100 == 0:
                    sys.stderr.write("Adding new bill #{}\n".format(num_new_bills))

        sys.stdout.write("Number of bills added: {}\n".format(num_new_bills))
        sys.stdout.write("Number of bills updated: {}\n".format(num_updated_bills))

        sys.stdout.write("DONE\n")

    except cm.GeoTag.DoesNotExist:
        sys.stdout.write("state not in geotags\n")
    finally:
        sys.stdout.flush()

def update_state_bulk(state_name, openstates_state_abbrev):
    """
    This method is deprecated
    Update state information using bulk data, which appears to be aggregiously outdated
    """
    tempdir = None
    try:
        tempdir = tempfile.mkdtemp()
        sys.stderr.write("temporary directory: {}\n".format(tempdir))
        workingdir = tempdir+"/openstates_data_workingdir"
        jsonzip = tempdir+"/state-json.zip"
        num_new_legislators = 0
        num_updated_legislators = 0
        num_legislator_exceptions = 0
        num_new_bills = 0
        num_updated_bills = 0
        num_bill_exceptions = 0

        sys.stdout.write(state_name+"\n")
        sys.stdout.flush()
        state_geotag = cm.GeoTag.objects.get(feature_type="SP", name=state_name)

        with open(jsonzip, "wb") as state_zip_file:
            sys.stdout.write("downloading...\n")
            pyopenstates.download_bulk_data(openstates_state_abbrev, state_zip_file)

        sys.stdout.write("unzipping...\n")
        zip_ref = zipfile.ZipFile(jsonzip, 'r')
        zip_ref.extractall(workingdir)
        zip_ref.close()

        legislator_files = os.listdir(workingdir+"/legislators")
        sys.stdout.write("number of legislators:"+str(len(legislator_files))+"\n")

        for f in legislator_files:
            with open(workingdir+"/legislators/"+f, 'r') as leg_file:
                leg_json = json.loads(leg_file.read())
                result = update_legislator(leg_json, state_geotag)
                if result == "update":
                    num_updated_legislators += 1
                elif result == "new":
                    num_new_legislators += 1

        sys.stdout.write("Number of legislators added: {}\n".format(num_new_legislators))
        sys.stdout.write("Number of legislators updated: {}\n".format(num_updated_legislators))
        sys.stdout.write("Number of exceptions updating a legislator: {}\n".format(num_legislator_exceptions))

        bill_files = [os.path.join(root, name) for root, dirs, files in os.walk(workingdir+"/bills") for name in files]
        sys.stdout.write("number of bills:"+str(len(bill_files))+"\n")

        for f in bill_files:
            with open(f, 'r') as bill_file:
                bill_json = json.loads(bill_file.read())
                result = update_bill(bill_json, state_geotag)
                if result == "update":
                    num_updated_bills += 1
                    if num_updated_bills % 100 == 0:
                        sys.stderr.write("Updating bill #{}\n".format(num_updated_bills))
                elif result == "new":
                    num_new_bills += 1
                    if num_new_bills % 100 == 0:
                        sys.stderr.write("Adding new bill #{}\n".format(num_new_bills))


        committee_files = os.listdir(workingdir+"/committees")
        sys.stdout.write("number of committees:"+str(len(committee_files))+"\n")
        sys.stdout.write("Number of bills added: {}\n".format(num_new_bills))
        sys.stdout.write("Number of bills updated: {}\n".format(num_updated_bills))
        sys.stdout.write("DONE\n")

    except cm.GeoTag.DoesNotExist:
        sys.stdout.write("state not in geotags\n")
    except zipfile.BadZipfile:
        sys.stdout.write("there was a problem reading this state's zipfile\n")
    finally:
        sys.stdout.flush()
        shutil.rmtree(tempdir)


@transaction.atomic
def update_legislator(leg_json, state_geotag):
    legislator_fields = {"name":"full_name", "photo_url":"photo_url", "webpage_url":"url", "chamber":"chamber", "district":"district", "open_states_leg_id":"id", "open_states_active":"active", "email":"email", "phone":"office_phone"}

    existing_leg = None
    try:
        existing_leg = LegislatorsProject.objects.get(open_states_leg_id = leg_json["id"])
    except LegislatorsProject.DoesNotExist:
        pass

    if existing_leg is None:
        p = LegislatorsProject()
        for i in legislator_fields.items():
            max_len = LegislatorsProject._meta.get_field(i[0]).max_length
            val = leg_json.get(i[1], None)
            p.__dict__[i[0]] = val if not isinstance(val, unicode) and not isinstance(val, str) else val[:max_len]

        p.open_states_state = state_geotag.name
        p.owner_profile = cm.get_default_user().userprofile
        p.save()
        p.tags.add(state_geotag.tag_ptr)
        ct.finalize_project(p, True)
        return "new"

    else: # check for updates to an existing legislator
        change_set = set()
        p = existing_leg
        for i in legislator_fields.items():
            max_len = LegislatorsProject._meta.get_field(i[0]).max_length
            val = leg_json.get(i[1], None)
            val = val if not isinstance(val, unicode) and not isinstance(val, str) else val[:max_len]
            if not p.__dict__[i[0]] == val:
                change_set.add(i[0])
                p.__dict__[i[0]] = val

        p.open_states_state = state_geotag.name
        if len(change_set) > 0:
            p.save()

        current_tags = p.tags.all()
        new_tags = set()
        new_tags.add(state_geotag.tag_ptr)
        if len(new_tags.symmetric_difference(current_tags)) > 0:
            p.tags.clear()
            p.tags.add(*new_tags)
            change_set.add("tags")

        #### finalize
        if "name" in change_set or "photo_url" in change_set or "tags" in change_set:
            sys.stderr.write("there are changes requiring item updates: {}\n".format(change_set))
            ct.finalize_project(p, True)                        
        if len(change_set) > 0:
            return "updated"

@transaction.atomic
def update_bill(bill_json, state_geotag):
    bill_fields = {"open_states_bill_id":"id", "name":"title", "bill_id":"bill_id"}
    bill_action_date_fields = {"first_action_date": "first", "last_action_date": "last", "passed_upper_date":"passed_upper", "passed_lower_date":"passed_lower", "signed_date":"signed"}
    bill_document_fields = {"url":"url", "name":"name", "mimetype":"mimetype"}

    existing_bill = None
    try:
        existing_bill = BillsProject.objects.get(open_states_bill_id = bill_json["id"])
    except BillsProject.DoesNotExist:
        pass

    if existing_bill is None:
        p = BillsProject()
        # sys.stderr.write("Bill title:{}\n".format(bill_json['title']))
        for i in bill_fields.items():
            max_len = BillsProject._meta.get_field(i[0]).max_length
            val = bill_json.get(i[1], None)
            p.__dict__[i[0]] = val if not isinstance(val, unicode) and not isinstance(val, str) else val[:max_len]

        for i in bill_action_date_fields.items():
            date_object = bill_json["action_dates"].get(i[1], None)
            if isinstance(date_object, unicode) or isinstance(date_object, str):
                date_string = date_object
                if " " in date_string:
                    date_string = date_string.split(" ")[0]
                p.__dict__[i[0]] = date_string
            elif isinstance(date_object, datetime.datetime):
                p.__dict__[i[0]] = date_object
            elif date_object is None:
                pass
            else:
                sys.stderr.write("update_bill. Don't know how to handle this date object:{}\n".format(date_object))

        p.owner_profile = cm.get_default_user().userprofile
        p.save()

        versions = bill_json["versions"]
        for v in versions:
            doc_openstates_id = v["doc_id"]
            existing_doc = None
            try:
                existing_doc = cm.ReferenceDocument.objects.get(external_api = "openstates", external_id=doc_openstates_id)
            except cm.ReferenceDocument.DoesNotExist:
                pass
            if existing_doc is None:
                doc = cm.ReferenceDocument()
                doc.external_api = "openstates"
                doc.external_id = doc_openstates_id
                for i in bill_document_fields.items():
                    max_len = cm.ReferenceDocument._meta.get_field(i[0]).max_length
                    val = v.get(i[1], None)
                    doc.__dict__[i[0]] = val if not isinstance(val, unicode) and not isinstance(val, str) else val[:max_len]

                doc.save()
                p.documents.add(doc)
            else:                
                p.documents.add(existing_doc)

        p.tags.add(state_geotag.tag_ptr)
        subjects = bill_json.get("subjects",[])
        for s in subjects:
            try:
                t = cm.Tag.objects.get(name=s, detail="Openstates Subject")
                p.tags.add(t)
            except cm.Tag.DoesNotExist:
                pass

        ct.finalize_project(p, True)                        
        return "new"

    else:
        change_set = set()
        p = existing_bill
        for i in bill_fields.items():
            max_len = BillsProject._meta.get_field(i[0]).max_length
            val = bill_json.get(i[1], None)
            val = val if not isinstance(val, unicode) and not isinstance(val, str) else val[:max_len]
            if not p.__dict__[i[0]] == val:
                change_set.add(i[0])
                p.__dict__[i[0]] = val

        for i in bill_action_date_fields.items():

            date_object = bill_json["action_dates"].get(i[1], None)
            current_val = p.__dict__[i[0]]
            if isinstance(date_object, unicode) or isinstance(date_object, str):
                date_string = date_object
                if " " in date_string:
                    date_string = date_string.split(" ")[0]

                if not str(current_val).strip() == date_string:
                    change_set.add(i[0])
                    p.__dict__[i[0]] = date_string

            elif isinstance(date_object, datetime.datetime):
                if current_val != date_object:
                    change_set.add(i[0])
                    p.__dict__[i[0]] = date_object

            elif date_object is None:
                if not current_val is None:
                    change_set.add(i[0])
                    p.__dict__[i[0]] = date_string
            else:
                sys.stderr.write("update_bill. Don't know how to handle this date object:{}\n".format(date_object))


        versions = bill_json["versions"]
        current_documents = p.documents.all()
        new_documents = set()
        for v in versions:
            doc_openstates_id = v["doc_id"]
            existing_doc = None
            try:
                existing_doc = cm.ReferenceDocument.objects.get(external_api = "openstates", external_id=doc_openstates_id)
            except cm.ReferenceDocument.DoesNotExist:
                pass
            if existing_doc is None:
                doc = cm.ReferenceDocument()
                doc.external_api = "openstates"
                doc.external_id = doc_openstates_id
                for i in bill_document_fields.items():
                    max_len = cm.ReferenceDocument._meta.get_field(i[0]).max_length
                    val = v.get(i[1], None)
                    doc.__dict__[i[0]] = val if not isinstance(val, unicode) and not isinstance(val, str) else val[:max_len]

                doc.save()
                new_documents.add(doc)
            else:
                new_documents.add(existing_doc)

        if len(new_documents.symmetric_difference(current_documents)) > 0:
            p.documents.clear()
            p.documents.add(*new_documents)
            change_set.add("documents")

        if len(change_set)>0:
            p.save()

        current_tags = p.tags.all()
        new_tags = set()
        new_tags.add(state_geotag.tag_ptr)
        subjects = bill_json.get("subjects",[])
        for s in subjects:
            try:
                t = cm.Tag.objects.get(name=s, detail="Openstates Subject")
                new_tags.add(t)
            except cm.Tag.DoesNotExist:
                sys.stderr.write("tag doesn't exist:{}\n".format(s))

        if len(new_tags.symmetric_difference(current_tags)) > 0:
            p.tags.clear()
            p.tags.add(*new_tags)
            change_set.add("tags")

        #### propagate project changes
        if "tags" in change_set or "name" in change_set or "last_action_date" in change_set:
            sys.stderr.write("there are changes requiring item updates to project {}: {}\n".format(p.id, change_set))

            sys.stderr.flush()
            ct.finalize_project(p, True)                        

        if len(change_set) > 0:
            return "updated"


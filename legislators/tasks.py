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

def get_task(task_name):
    function, state_name, openstates_state_abbrev = task_name.split("|")
    if function == "update_state":
        return lambda : update_state(state_name, openstates_state_abbrev)
    

def update_state(state_name, openstates_state_abbrev):
    """
    This function currently uses the file system to store temporary files, so only one can be run at a time
    """
    tempdir = None
    try:
        tempdir = tempfile.mkdtemp()
        sys.stderr.write("temporary directory: {}\n".format(tempdir))
        workingdir = tempdir+"/openstates_data_workingdir"
        jsonzip = tempdir+"/state-json.zip"
        num_new_legislators = 0
        num_updated_legislators = 0
        num_new_bills = 0
        num_updated_bills = 0

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
            p.__dict__[i[0]] = leg_json.get(i[1], None)

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
            if not p.__dict__[i[0]] == leg_json.get(i[1], None):
                change_set.add(i[0])
            p.__dict__[i[0]] = leg_json.get(i[1], None)

        p.open_states_state = state_geotag.name
        p.owner_profile = cm.get_default_user().userprofile
        p.save()

        current_tags = p.tags.all()
        new_tags = set()
        new_tags.add(state_geotag.tag_ptr)
        if len(new_tags.symmetric_difference(current_tags)) > 0:
            p.tags.clear()
            p.tags.add(*new_tags)
            change_set.add("tags")

        #### propagate project changes
        if "tags" in change_set or "name" in change_set:
            sys.stderr.write("changes are significant, we have to de-activate and re-create items for this project")
            sys.stderr.flush()
            # de-activate all existing items and re-create items for this project
            LegislatorsItem.objects.filter(participation_project=p, is_active=True).update(is_active=False)

        #### finalize
        ct.finalize_project(p, True)                        
        if len(change_set) > 0:
            sys.stderr.write("there are changes: {}\n".format(change_set))
            return "updated"

@transaction.atomic
def update_bill(bill_json, state_geotag):
    bill_fields = {"open_states_bill_id":"id", "name":"title", "bill_id":"bill_id"}
    bill_action_date_fields = {"first_action_date": "first", "last_action_date": "last", "passed_upper_date":"passed_upper", "passed_lower_date":"passed_lower", "signed_date":"signed"}

    existing_bill = None
    try:
        existing_bill = BillsProject.objects.get(open_states_bill_id = bill_json["id"])
    except BillsProject.DoesNotExist:
        pass

    if existing_bill is None:
        p = BillsProject()
        # sys.stderr.write("Bill title:{}\n".format(bill_json['title']))
        for i in bill_fields.items():
            p.__dict__[i[0]] = bill_json.get(i[1], None)[:500]

        for i in bill_action_date_fields.items():
            date_string = bill_json["action_dates"].get(i[1], None)
            if not date_string is None:
                # sys.stdout.write("{}: {}\n".format(i[1], date_string))
                if " " in date_string:
                    date_string = date_string.split(" ")[0]
                p.__dict__[i[0]] = date_string

        p.owner_profile = cm.get_default_user().userprofile
        p.save()

        p.tags.add(state_geotag.tag_ptr)
        subjects = bill_json["subjects"]
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
            if not p.__dict__[i[0]] == bill_json.get(i[1], None)[:500]:
                change_set.add(i[0])
            p.__dict__[i[0]] = bill_json.get(i[1], None)[:500]

        for i in bill_action_date_fields.items():
            date_string = bill_json["action_dates"].get(i[1], None)
            current_val = p.__dict__[i[0]]
            if p.__dict__[i[0]] is None and not date_string is None:
                change_set.add(i[0])
                p.__dict__[i[0]] = date_string

            elif date_string is None and not p.__dict__[i[0]] is None:
                change_set.add(i[0])
                p.__dict__[i[0]] = date_string

            elif not date_string is None:
                if " " in date_string:
                    date_string = date_string.split(" ")[0]
                if not str(current_val).strip() == date_string:
                    change_set.add(i[0])
                    p.__dict__[i[0]] = date_string


        p.owner_profile = cm.get_default_user().userprofile
        p.save()

        current_tags = p.tags.all()
        new_tags = set()
        new_tags.add(state_geotag.tag_ptr)
        subjects = bill_json["subjects"]
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
        if "tags" in change_set or "name" in change_set:
            sys.stderr.write("changes are significant, we have to de-activate and re-create items for this project")
            sys.stderr.flush()
            # de-activate all existing items and re-create items for this project
            BillsItem.objects.filter(participation_project=p, is_active=True).update(is_active=False)

        #### finalize
        ct.finalize_project(p, True)                        

        if len(change_set) > 0:
            sys.stderr.write("there are changes: {}\n".format(change_set))
            return "update"


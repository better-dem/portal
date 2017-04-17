from django.core.management.base import BaseCommand, CommandError
from legislators.models import LegislatorsProject, LegislatorsItem, BillsProject, BillsItem
import core.models as cm
import core.tasks as ct

import argparse
import datetime
import sys
import pyopenstates
import zipfile
import os
import json

class Command(BaseCommand):
    help = """
    A utility to update all legislators using the openstates API
    usage: python manage.py legislators_update -m <mode>
    """

    def handle(self, *args, **options):
        mode = options["mode"]
        workingdir = "openstates_data_workingdir"
        jsonzip = "state-json.zip"
        assert mode in ["run", "dry-run"]

        num_new_legislators = 0
        num_updated_legislators = 0
        num_new_bills = 0
        num_updated_bills = 0
        num_state_errors = 0
        num_legislator_errors = 0

        metadata = pyopenstates.get_metadata()
        tags = cm.GeoTag.objects.filter(feature_type="SP")
        sys.stdout.write("number of state / province tags:"+unicode(len(tags))+"\n")
        sys.stdout.write("state names:"+unicode([t.name for t in tags])+"\n")
        sys.stdout.flush()
        for state in metadata:
            sys.stdout.write("deleting existing state data...\n")
            sys.stdout.flush()
            os.system("rm -rf "+workingdir+"/*")
            os.system("rm "+jsonzip)
            sys.stdout.write(state["name"]+"\n")
            sys.stdout.flush()
            tag = None
            try:
                tag = cm.GeoTag.objects.get(feature_type="SP", name=state["name"])
            except:
                num_state_errors += 1
                sys.stdout.write("state not in geotags\n")
                continue

            try:
                with open(jsonzip, "wb") as state_zip_file:
                    sys.stdout.write("downloading...\n")
                    pyopenstates.download_bulk_data(state["abbreviation"], state_zip_file)

                sys.stdout.write("unzipping...\n")
                zip_ref = zipfile.ZipFile(jsonzip, 'r')
                zip_ref.extractall(workingdir)
                zip_ref.close()

            except zipfile.BadZipfile:
                num_state_errors += 1
                sys.stdout.write("there was a problem reading this state's zipfile\n")
                sys.stdout.flush()
                continue

            sys.stdout.write("results:\n")
            sys.stdout.write("contents:"+str(os.listdir(workingdir))+"\n")
            legislator_files = os.listdir(workingdir+"/legislators")
            sys.stdout.write("number of legislators:"+str(len(legislator_files))+"\n")

            for f in legislator_files:
                with open(workingdir+"/legislators/"+f, 'r') as leg_file:
                    leg_json = json.loads(leg_file.read())
                    legislator_fields = {"name":"full_name", "photo_url":"photo_url", "webpage_url":"url", "chamber":"chamber", "district":"district", "open_states_leg_id":"id", "open_states_active":"active", "email":"email", "phone":"office_phone"}

                    existing_leg = None
                    try:
                        existing_leg = LegislatorsProject.objects.get(open_states_leg_id = leg_json["id"])
                    except LegislatorsProject.DoesNotExist:
                        pass

                    if mode == "run" and existing_leg is None:
                        p = LegislatorsProject()
                        for i in legislator_fields.items():
                            p.__dict__[i[0]] = leg_json.get(i[1], None)
                        
                        p.open_states_state = tag.name
                        p.owner_profile = cm.get_default_user().userprofile
                        p.save()
                        p.tags.add(tag)
                        ct.finalize_project(p)
                        num_new_legislators += 1

                    elif mode == "run": # check for updates to an existing legislator
                        change_set = set()
                        p = existing_leg
                        for i in legislator_fields.items():
                            if not p.__dict__[i[0]] == leg_json.get(i[1], None):
                                change_set.add(i[0])
                            p.__dict__[i[0]] = leg_json.get(i[1], None)

                        p.open_states_state = tag.name
                        p.owner_profile = cm.get_default_user().userprofile
                        p.save()

                        current_tags = set([x.id for x in p.tags.all()])
                        new_tags = set()
                        new_tags.add(tag.id)
                        if len(new_tags.symmetric_difference(current_tags)) > 0:
                            p.tags.clear()
                            p.tags.add(tag)
                            change_set.add("tags")

                        if len(change_set) > 0:
                            sys.stderr.write("there are changes: {}\n".format(change_set))
                            num_updated_legislators += 1

                        #### propagate project changes
                        if "tags" in change_set or "name" in change_set:
                            sys.stderr.write("changes are significant, we have to de-activate and re-create items for this project")
                            sys.stderr.flush()
                            # de-activate all existing items and re-create items for this project
                            LegislatorsItem.objects.filter(participation_project=p, is_active=True).update(is_active=False)

                        #### finalize
                        ct.finalize_project(p)                        

            bill_files = [os.path.join(root, name) for root, dirs, files in os.walk(workingdir+"/bills") for name in files]
            sys.stdout.write("number of bills:"+str(len(bill_files))+"\n")
            sys.stdout.write("some bills:"+str(bill_files[:10])+"\n")
            bill_fields = {"open_states_bill_id":"id", "name":"title", "bill_id":"bill_id"}
            bill_action_date_fields = {"first_action_date": "first", "last_action_date": "last", "passed_upper_date":"passed_upper", "passed_lower_date":"passed_lower", "signed_date":"signed"}
            for f in bill_files:
                with open(f, 'r') as bill_file:
                    bill_json = json.loads(bill_file.read())

                    existing_bill = None
                    try:
                        existing_bill = BillsProject.objects.get(open_states_bill_id = bill_json["id"])
                    except BillsProject.DoesNotExist:
                        pass

                    if mode == "run" and existing_bill is None:
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

                        p.tags.add(tag)
                        subjects = bill_json["subjects"]
                        for s in subjects:
                            try:
                                t = cm.Tag.objects.get(name=s, detail="Openstates Subject")
                                p.tags.add(t)
                            except cm.Tag.DoesNotExist:
                                pass

                        ct.finalize_project(p)                        
                        num_new_bills += 1
                        if num_new_bills % 1000 == 0:
                            sys.stderr.write("Adding new bill #{}\n".format(num_new_bills))

                    elif mode == "run":
                        p = existing_bill
                        ct.finalize_project(p)                        
                    

            committee_files = os.listdir(workingdir+"/committees")
            sys.stdout.write("number of committees:"+str(len(committee_files))+"\n")
            sys.stdout.flush()

            break

        os.system("rm -rf "+workingdir+"/*")
        os.system("rm "+jsonzip)

        sys.stdout.write("Number of legislators added: {}\n".format(num_new_legislators))
        sys.stdout.write("Number of legislators updated: {}\n".format(num_updated_legislators))
        sys.stdout.write("Number of state errors: {}\n".format(num_state_errors))
        sys.stdout.write("Number of legislator errors: {}\n".format(num_legislator_errors))
        sys.stdout.write("Number of bills added: {}\n".format(num_new_bills))
        sys.stdout.write("Number of bills updated: {}\n".format(num_updated_bills))
        sys.stdout.write("DONE\n")
        sys.stdout.flush()
         
    def add_arguments(self, parser):
        parser.add_argument('-m', '--mode', required=True, type=str, help="mode", action='store')


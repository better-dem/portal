from django.core.management.base import BaseCommand, CommandError
from core import models as cm

import argparse
import datetime
import sys
import pyopenstates
import zipfile
import os

class Command(BaseCommand):
    help = """
    A utility to update all legislators using the openstates API
    usage: python manage.py legislators_update -m <mode>
    """

    def handle(self, *args, **options):
        mode = options["mode"]
        workingdir = "openstates_data_workingdir"
        jsonzip = "state-json.zip"

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
                sys.stdout.write("there was a problem reading this state's zipfile\n")
                sys.stdout.flush()
                continue

            sys.stdout.write("results:\n")
            sys.stdout.write("contents:"+str(os.listdir(workingdir))+"\n")
            legislator_files = os.listdir(workingdir+"/legislators")
            sys.stdout.write("number of legislators:"+str(len(legislator_files))+"\n")
            bill_files = os.listdir(workingdir+"/bills")
            sys.stdout.write("number of bills:"+str(len(bill_files))+"\n")
            committee_files = os.listdir(workingdir+"/committees")
            sys.stdout.write("number of committees:"+str(len(committee_files))+"\n")
            sys.stdout.flush()

        sys.stdout.write("DONE\n")
        sys.stdout.flush()
        os.system("rm -rf "+workingdir+"/*")
        os.system("rm "+jsonzip)
         
    def add_arguments(self, parser):
        parser.add_argument('-m', '--mode', required=True, type=str, help="mode", action='store')


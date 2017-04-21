from django.core.management.base import BaseCommand, CommandError
from legislators.models import LegislatorsProject, LegislatorsItem, BillsProject, BillsItem
import core.models as cm
import core.tasks as ct
from django.db import transaction
from django.utils import timezone

import argparse
import sys
import pyopenstates
import zipfile
import os
import json
import core.models as cm

class Command(BaseCommand):
    help = """
    Creates job status objects for each of the states in openstates.
    A utility to update all legislators using the openstates API
    usage: python manage.py legislators_update
    """

    def handle(self, *args, **options):
        metadata = pyopenstates.get_metadata()
        num_jobs_created = 0
        for state in metadata:
            obj, created = cm.LongJobState.objects.get_or_create(
                app_name = "legislators",
                name="update_state|{}|{}".format(state["name"], state["abbreviation"]),
                defaults={"job_period":60*60*24, "job_timeout": 60*60, "most_recent_update": timezone.now() - timezone.timedelta(24*60*60)}
            )
            if created:
                sys.stdout.write("Created job for state: {}\n".format(state["name"]))
                sys.stdout.flush()
                num_jobs_created += 1
        sys.stdout.write("Created {} jobs\n".format(num_jobs_created))
        sys.stdout.write("DONE\n")
        sys.stdout.flush()



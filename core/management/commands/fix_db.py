from django.core.management.base import BaseCommand, CommandError
from core import models as cm

import argparse
import datetime
import sys


class Command(BaseCommand):
    help = """
    A DANGEROUS utility for editing the DB to fix known issues due to botched migrations, etc.
    ALWAYS run in display mode before running in fix mode
    Display or repair depending on mode
    usage: python manage.py fix_db -t <trouble type> -m <mode>
    """

    def handle(self, *args, **options):
        trouble_type = options["troubletype"]
        mode = options["mode"]

        if mode == "fix":
            if trouble_type=="abstract_items":
                for o in cm.ParticipationItem.objects.all():
                    try:
                        i = o.get_inherited_instance()
                    except:
                        sys.stdout.write("participation item found whose inherited instance can't be determined:{}".format(o.name)+"\n")
                        sys.stdout.flush()
                        sys.stdout.write("deleting item\n")
                        o.delete()
                        sys.stdout.write("object deleted\n")

            elif trouble_type=="abstract_projects":
                for o in cm.ParticipationProject.objects.all():
                    try:
                        i = o.get_inherited_instance()
                    except:
                        sys.stdout.write("participation project found whose inherited instance can't be determined:{}".format(o.name)+"\n")
                        sys.stdout.flush()
                        sys.stdout.write("deleting project\n")
                        o.delete()
                        sys.stdout.write("object deleted\n")

            else:
                raise Exception("unknown trouble type:"+str(trouble_type))
        elif mode == "display":
            if trouble_type=="abstract_items":
                for o in cm.ParticipationItem.objects.all():
                    try:
                        i = o.get_inherited_instance()
                    except:
                        sys.stdout.write("participation item found whose inherited instance can't be determined:{}".format(o.name)+"\n")
                        sys.stdout.flush()

            elif trouble_type=="abstract_projects":
                for o in cm.ParticipationProject.objects.all():
                    try:
                        i = o.get_inherited_instance()
                    except:
                        sys.stdout.write("participation project found whose inherited instance can't be determined:{}".format(o.name)+"\n")
                        sys.stdout.flush()

            else:
                raise Exception("unknown trouble type:"+str(trouble_type))
        else:
            raise Exception("unknown mode:"+str(mode))
        sys.stdout.write("DONE\n")
        sys.stdout.flush()
         
    def add_arguments(self, parser):
        parser.add_argument('-m', '--mode', required=True, type=str, help="mode", action='store')
        parser.add_argument('-t', '--troubletype', required=True, type=str, help="trouble type", action='store')

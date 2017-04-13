from django.core.management.base import BaseCommand, CommandError
from core import models as cm

import argparse
import datetime
import sys


class Command(BaseCommand):
    help = """
    A utility to update all legislators
    usage: python manage.py legislators_update -m <mode>
    """

    def handle(self, *args, **options):
        mode = options["mode"]

        if mode == "fix":
            for o in cm.ParticipationProject.objects.all():
                try:
                    i = o.get_inherited_instance()
                except:
                    sys.stdout.write("participation project found whose inherited instance can't be determined:{}".format(o.name)+"\n")
                    sys.stdout.flush()
                    sys.stdout.write("deleting project\n")
                    o.delete()
                    sys.stdout.write("object deleted\n")
        elif mode == "display":
            for o in cm.ParticipationProject.objects.all():
                try:
                    i = o.get_inherited_instance()
                except:
                    sys.stdout.write("participation project found whose inherited instance can't be determined:{}".format(o.name)+"\n")
                    sys.stdout.flush()

        else:
            raise Exception("unknown mode:"+str(mode))
        sys.stdout.write("DONE\n")
        sys.stdout.flush()
         
    def add_arguments(self, parser):
        parser.add_argument('-m', '--mode', required=True, type=str, help="mode", action='store')
        parser.add_argument('-t', '--troubletype', required=True, type=str, help="trouble type", action='store')

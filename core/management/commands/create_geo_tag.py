from django.core.management.base import BaseCommand, CommandError
from core import models as cm

import argparse
import datetime
import sys
import csv

class Command(BaseCommand):
    help = """
    Create geo-tags from uscitieslist.org csv file. (must be bought separately)
    """

    def handle(self, *args, **options):

        filename = options["filename"]
        with open(filename) as f:
            reader = csv.reader(f, delimiter=",", quotechar='"')
            first_row = True
            for row in reader:
                if not first_row:
                    name = row[1]
                    state = row[4]
                    lat = row[7]
                    lon = row[8]
                    population = row[10]
                    median_income = row[12]
                    land_area = row[13]
                    
                    print lon, lat, "POINT({} {})".format(str(lon), str(lat))

                    t = cm.GeoTag.objects.create(tag_name=name, point="POINT({} {})".format(str(lon), str(lat)))
                    t.save()
                    
                first_row = False
         
    def add_arguments(self, parser):
        parser.add_argument('-f', '--filename', required=True, type=str, help="csv filename", action='store')

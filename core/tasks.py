from __future__ import absolute_import
import core.models as cm
import csv
import sys
import os
from celery import shared_task

@shared_task
def marco():
    sys.stdout.write("polo\n")
    sys.stdout.flush()

@shared_task
def insert_csv1():
    num_changes = 0
    with open("tmp.csv") as f:
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

                if not cm.GeoTag.objects.filter(name=name, detail=state+", United States").exists():
                    t = cm.GeoTag.objects.create(name=name, detail=state+", United States",point="POINT({} {})".format(str(lon), str(lat)))
                    t.save()
                    num_changes += 1

            first_row = False
    os.remove("tmp.csv")
    sys.stdout.write("Done updating GeoTags\n")
    sys.stdout.write("Number of changes: "+str(num_changes)+"\n")
    sys.stdout.flush()

from __future__ import absolute_import
import core.models as cm
import csv
import sys
from celery import shared_task
from django.core.files.storage import default_storage

@shared_task
def marco():
    sys.stdout.write("polo\n")
    sys.stdout.flush()

@shared_task
def insert_csv1(small_test):
    filename = "/uploads/misc/tmp.csv"
    sys.stdout.write("Processing csv for file: "+str(filename)+"\n")
    i = 0
    num_changes = 0
    with default_storage.open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=",", quotechar='"')
        first_row = True
        for row in reader:
            if small_test and i > 100:
                break
            if i % 1000 == 0:
                sys.stdout.write("Processing row "+str(i)+"\n")

            i += 1
            if first_row:
                first_row = False
                continue

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

    default_storage.delete(filename)
    sys.stdout.write("Done updating GeoTags\n")
    sys.stdout.write("Number of rows processed: "+str(i)+"\n")
    sys.stdout.write("Number of changes: "+str(num_changes)+"\n")
    sys.stdout.flush()

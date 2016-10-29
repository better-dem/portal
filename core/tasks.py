from __future__ import absolute_import
import core.models as cm
import csv
import sys
from celery import shared_task
from django.core.files.storage import default_storage
import itertools

### Begin: Tasks for loading data files & updating the database

@shared_task
def insert_uscitieslist_v0(small_test):
    filename = "/uploads/misc/tmp"
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
                t = cm.GeoTag.objects.create(name=name, feature_type=cm.GeoTag.CITY, detail=state+", United States",point="POINT({} {})".format(str(lon), str(lat)))
                t.save()
                num_changes += 1
            else:
                # update feature type if its missing
                # assume there's only one match
                obj = cm.GeoTag.objects.filter(name=name, detail=state+", United States")[0]
                if obj.feature_type == cm.GeoTag.UNKNOWN:
                    obj.feature_type = cm.GeoTag.CITY
                    obj.save()
                    num_changes += 1

    default_storage.delete(filename)
    sys.stdout.write("Done updating GeoTags\n")
    sys.stdout.write("Number of rows processed: "+str(i)+"\n")
    sys.stdout.write("Number of changes: "+str(num_changes)+"\n")
    sys.stdout.flush()

@shared_task
def insert_usa_and_states(small_test):
    filename = "/uploads/misc/tmp"
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

            name = row[0]
            feature_type = row[1]
            detail = row[2]

            if not cm.GeoTag.objects.filter(name=name, feature_type=feature_type, detail=detail).exists():
                t = cm.GeoTag.objects.create(name=name, feature_type=feature_type, detail=detail)
                t.save()
                num_changes += 1

    default_storage.delete(filename)
    sys.stdout.write("Done updating GeoTags\n")
    sys.stdout.write("Number of rows processed: "+str(i)+"\n")
    sys.stdout.write("Number of changes: "+str(num_changes)+"\n")
    sys.stdout.flush()

### Begin: Regular Background tasks

@shared_task
def item_update():
    apps = cm.get_registered_participation_apps()
    num_items_created = 0
    for app in apps:
        project_model = cm.get_app_project_models(app)[0]
        projects = project_model.objects.all()
        for p in projects:
            num_items_created += p.update_items()
            
    sys.stdout.write("number of items created: "+str(num_items_created))
    sys.stdout.flush()

@shared_task
def feed_update():
    items = cm.ParticipationItem.objects.all()
    users = cm.User.objects.filter(is_active=True)
    num_matches_created = 0
    for (i, u) in itertools.product(items, users):
        if cm.FeedMatch.objects.filter(participation_item=i, user_profile=u.userprofile).count()==0:
            match = cm.FeedMatch()
            match.user_profile = u.userprofile
            match.participation_item = i
            match.save()
            num_matches_created += 1

    sys.stdout.write("number of matches created: "+str(num_matches_created))
    sys.stdout.flush()

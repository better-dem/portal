from __future__ import absolute_import
import core.models as cm
import csv
import sys
import traceback
import requests
from PIL import Image
import tempfile
import io
import shutil

from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded
from django.core.files.storage import default_storage
import itertools
from django.db.models.signals import post_save
from django.contrib.gis.geos import Point        
from django.db import transaction
from django.utils import timezone
from django.db.models import F, ExpressionWrapper, DurationField
import redis

def finalize_project(project, current_process=False):
    """
    update items and recommendations for a new or newly-edited project
    optional flag current_process allows this to be run in the current process instead of queued and run by celery worker
    """
    if current_process:
        transaction.on_commit(lambda: item_update(project.pk))
    else:
        transaction.on_commit(lambda: item_update.delay(project.pk))

### Tasks to manage long-running background jobs
@shared_task(expires=1)
def pick_long_job():
    now = timezone.now()
    epoch = timezone.datetime.fromtimestamp(0, tz=timezone.utc)
    jobs = cm.LongJobState.objects.all()
    try:
        furthest_overdue_job = sorted(jobs, key=lambda j: (now - j.most_recent_update).total_seconds() - j.job_period)[-1]
        if (now - furthest_overdue_job.most_recent_update).total_seconds() - furthest_overdue_job.job_period > 0:
            job_timeout = furthest_overdue_job.job_timeout
            run_long_job.apply_async(args=[furthest_overdue_job.id, job_timeout], soft_time_limit=job_timeout, time_limit=job_timeout+5)
        else:
            sys.stderr.write("job isn't overdue\n")
    except IndexError:
        sys.stderr.write("No jobs in database\n")
        return

@shared_task(expires=3)
def run_long_job(job_state_id, lock_timeout):
    now = timezone.now()
    lock = redis.Redis().lock("PORTAL_LONGJOB_LOCK", blocking_timeout=0, timeout=lock_timeout)
    lock_acquired = lock.acquire()    
    if lock_acquired:
        try:
            sys.stderr.write("long job lock acquired, running job\n")
            furthest_overdue_job = cm.LongJobState.objects.get(id=job_state_id)    
            furthest_overdue_job.most_recent_update = now
            furthest_overdue_job.save()
            task = cm.get_task_for_job_state(furthest_overdue_job) # task should just be a function, not a celery task
            task()
        except SoftTimeLimitExceeded as e:
            # currently no special handling of soft time limits
            traceback.print_exc()
        except Exception as e:
            traceback.print_exc()
        finally:
            lock.release()
        
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
            county = row[2]
            state = row[4]
            lat = row[7]
            lon = row[8]
            population = row[10]
            median_income = row[12]
            land_area = row[13]

            if not cm.GeoTag.objects.filter(name=name, point__distance_lte=(Point(float(lon), float(lat)), 1000)).exists():
                t = cm.GeoTag.objects.create(name=name, feature_type=cm.GeoTag.CITY, detail=county+", "+state+", United States", point="POINT({} {})".format(str(lon), str(lat)))
                t.save()
                num_changes += 1
            else:
                # update feature type if its missing
                # assume there's only one match
                obj = cm.GeoTag.objects.filter(name=name, point__distance_lte=(Point(float(lon), float(lat)), 1000))[0]
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
def insert_states(small_test):
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


@shared_task
def insert_openstates_subjects(small_test):
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

            if not cm.Tag.objects.filter(name=name, detail="Openstates Subject").exists():
                t = cm.Tag.objects.create(name=name, detail="Openstates Subject")
                t.save()
                num_changes += 1

    default_storage.delete(filename)
    sys.stdout.write("Done updating Openstates Subjects\n")
    sys.stdout.write("Number of rows processed: "+str(i)+"\n")
    sys.stdout.write("Number of changes: "+str(num_changes)+"\n")
    sys.stdout.flush()


### Begin: Regular Background tasks
@shared_task
def item_update(project_id):
    p = cm.ParticipationProject.objects.get(pk=project_id).get_inherited_instance()
    item_ids = p.update_items()
    num_items_created = len(item_ids)
    for item_id in item_ids:
        i = cm.ParticipationItem.objects.get(pk=item_id)


@shared_task
def scrape_image_and_set_field(url, projectid, itemid, field_name):
    """
    Scrapes an image url and puts the local image into the appropriate field.
    Uses the core.ParticipationProject / core.ParticipationItem .get_inherited_instance()
    """
    extension = "JPEG"

    type_string = None
    obj = None
    if not projectid is None and not itemid is None:
        raise Exception("Exactly one of the params projectid / itemid must be null")
    if not projectid is None:
        type_string = "project"
        obj = cm.ParticipationProject.objects.get(id=projectid).get_inherited_instance()
    else:
        type_string = "item"
        obj = cm.ParticipationItem.objects.get(id=itemid).get_inherited_instance()

    date_string = ''.join([ch for ch in str(timezone.now()) if ch.isalnum() or ch in ["-", "."]])
    filename = "uploads/scraped_images/{}_{}_{}_{}.{}".format(date_string, type_string, obj.id, field_name, extension)

    req = requests.get(url)
    if req.status_code != requests.codes.ok:
        sys.stderr.write(u"couldn't fnd image: {}\n".format(url))
        return
    img=None
    try:
        img = Image.open(io.BytesIO(req.content))
        bio = io.BytesIO()
        img.convert('RGB').save(bio, extension)
        bio.seek(0)

        with default_storage.open(filename, 'wb') as f:
            f.write(bio.read())

        obj.__dict__[field_name] = filename
        obj.save()
        sys.stderr.write(u"{} {} new image, scraped from: {}\n".format(type_string, obj.id, url))

    except:
        sys.stderr.write(u"PIL couldn't read this image: {}\n".format(url))

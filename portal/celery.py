from __future__ import absolute_import
import os
from celery import Celery
import sys
from kombu import Queue

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portal.settings')

from django.conf import settings

app = Celery('portal')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.conf.task_routes = {'core.tasks.run_long_job': {'queue':'long_job'}}

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

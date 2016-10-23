import time
import os
import sys
from django.core.management import execute_from_command_line
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portal.settings")

while True:
    execute_from_command_line(['manage.py', 'item_update'])
    execute_from_command_line(['manage.py', 'feed_update'])
    time.sleep(3)

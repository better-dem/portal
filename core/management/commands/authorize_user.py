from django.core.management.base import BaseCommand, CommandError
from core import models as cm
from django.contrib.auth.models import User, Permission


import argparse
import datetime
import sys


class Command(BaseCommand):
    help = """
    Authorize user to administer an app
    usage: python manage.py authorize_user -u <username> -a <app name>
    """

    def handle(self, *args, **options):

        username = options["username"]
        app_name = options["participationapp"]
        
        app = cm.get_app_by_name(app_name.lower())
        user = User.objects.get(username=username)
        perm = cm.get_provider_permission(app)

        user.user_permissions.add(perm)
         
    def add_arguments(self, parser):
        parser.add_argument('-u', '--username', required=True, type=str, help="username", action='store')
        parser.add_argument('-p', '--participationapp', required=True, type=str, help="app name", action='store')

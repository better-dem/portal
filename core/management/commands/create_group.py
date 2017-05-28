from django.core.management.base import BaseCommand, CommandError
from core import models as cm
from django.contrib.auth.models import User, Permission


import argparse
import datetime
import sys


class Command(BaseCommand):
    help = """
    Create a group. 
    name the group's owner, specify the group type, and limit the number of members
    usage: python manage.py create_group -o <owner's username> -n <group name> -s <max group size> -t <group type>
    """

    def handle(self, *args, **options):

        owner_username = options["owner"]
        groupname = options["groupname"]
        size = options["max_group_size"]
        typ = options["type"]

        group = cm.UserGroup(name=groupname, owner=User.objects.get(username=owner_username).userprofile, group_type=typ, max_invitations=size)
        group.save()
         
    def add_arguments(self, parser):
        parser.add_argument('-o', '--owner', required=True, type=str, help="group owner username", action='store')
        parser.add_argument('-n', '--groupname', required=True, type=str, help="group name", action='store')
        parser.add_argument('-s', '--max_group_size', required=True, type=int, help="max group size", action='store')
        parser.add_argument('-t', '--type', required=True, type=str, help="group type", action='store')

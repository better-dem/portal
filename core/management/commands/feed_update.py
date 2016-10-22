from django.core.management.base import BaseCommand, CommandError
from core import models as cm
from django.contrib.auth.models import User, Permission
import itertools

class Command(BaseCommand):
    help = """
    Update feed match tables by creating new matches
    usage: python manage.py feed_update
    """

    def handle(self, *args, **options):

        # for each item:
        # for each user:
        # create a match if there isn't one yet
        items = cm.ParticipationItem.objects.all()
        users = User.objects.filter(is_active=True)
        num_matches_created = 0
        for (i, u) in itertools.product(items, users):
            if cm.FeedMatch.objects.filter(participation_item=i, user_profile=u.userprofile).count()==0:
                match = cm.FeedMatch()
                match.user_profile = u.userprofile
                match.participation_item = i
                match.save()
                num_matches_created += 1

        self.stdout.write("number of matches created: "+str(num_matches_created))
        self.stdout.flush()

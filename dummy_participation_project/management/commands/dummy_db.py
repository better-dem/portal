from django.core.management.base import BaseCommand, CommandError
from dummy_participation_project.models import DummyProject, DummyItem
from core.models import UserProfile, FeedMatch
from django.contrib.auth.models import Permission

class Command(BaseCommand):
    help = 'Create dummy data'

    def handle(self, *args, **options):
        DummyProject.objects.all().delete()
        DummyItem.objects.all().delete()

        p1 = DummyProject()
        p1.name = "this is a dum project"
        p1.owner_profile = UserProfile.objects.all()[0]
        p1.save()

        

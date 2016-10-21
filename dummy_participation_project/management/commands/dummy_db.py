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

        i1 = DummyItem()
        i1.name = "I1-Awesome"
        i1.participation_project = p1
        i1.save()

        i2 = DummyItem()
        i2.name = "IU2-Moderate"
        i2.participation_project = p1
        i2.save()


        for user in UserProfile.objects.all():
            for item in DummyItem.objects.all():
                m = FeedMatch()
                m.participation_item = item
                m.user_profile = user
                m.save()

        self.stdout.write("number of feedmatches:" + str(FeedMatch.objects.all().count()))
        

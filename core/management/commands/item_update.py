from django.core.management.base import BaseCommand, CommandError
from core import models as cm
from django.contrib.auth.models import User, Permission

class Command(BaseCommand):
    help = """
    Create items for projects according to each project's rules for doing so
    usage: python manage.py item_update
    """

    def handle(self, *args, **options):

        apps = cm.get_registered_participation_apps()
        num_items_created = 0
        for app in apps:
            project_model = cm.get_app_project_models(app)[0]
            projects = project_model.objects.all()
            for p in projects:
                num_items_created += p.update_items()

        self.stdout.write("number of items created: "+str(num_items_created))
        self.stdout.flush()


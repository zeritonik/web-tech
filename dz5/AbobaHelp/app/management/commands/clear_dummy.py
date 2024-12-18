from django.core.management.base import BaseCommand

from app.models import User, Tag

class Command(BaseCommand):
    help = 'Deletes all dummy records'

    def handle(self, *args, **options):
        try:
            User.objects.filter(username__startswith="dummy").delete()
            Tag.objects.filter(name__startswith="dummy").delete()
            print("Deleted dummy records")
        except Exception as e:
            print(e)
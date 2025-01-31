from django.core.management.base import BaseCommand
from tv_programs.models import TVProgram
class Command(BaseCommand):
    help = 'Import films from json file'

    def handle(self, *args, **options):
        TVProgram.objects.all().delete()
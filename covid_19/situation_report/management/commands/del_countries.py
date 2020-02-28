from django.core.management.base import BaseCommand
from situation_report.models import Place


class Command(BaseCommand):

    def handle(self, *args, **options):
        Place.objects.all().delete()

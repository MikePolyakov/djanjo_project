from django.core.management.base import BaseCommand
from situation_report_app.update import update


class Command(BaseCommand):

    def handle(self, *args, **options):
        update()

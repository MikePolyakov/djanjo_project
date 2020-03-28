from django.core.management.base import BaseCommand
from situation_report_app.update_statistic import update_statistic


class Command(BaseCommand):

    def handle(self, *args, **options):
        update_statistic()

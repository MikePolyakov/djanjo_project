import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from situation_report.models import Place


class Command(BaseCommand):

    def handle(self, *args, **options):

        domain = 'https://www.who.int'
        url = f'{domain}/countries/en/'

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        countries = soup.find('div', class_="col_1-1-1_1").find_all('span')
        for each in countries:
            if not Place.objects.filter(name=each.text).exists():
                Place.objects.create(name=each.text)

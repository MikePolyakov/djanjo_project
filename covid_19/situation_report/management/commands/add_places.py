from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from situation_report.models import Place


class Command(BaseCommand):

    def handle(self, *args, **options):

        # в бд добавляем страны
        domain = 'https://www.who.int'
        url = f'{domain}/countries/en/'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        countries = soup.find('div', class_="col_1-1-1_1").find_all('span')
        country_added = 0
        for each in countries:
            if not Place.objects.filter(place_name=each.text).exists():
                Place.objects.create(place_name=each.text)
                country_added += 1

        total_countries = Place.objects.all()

        print(f'added {country_added}')
        print(f'total number of countries = {len(total_countries)}')

from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from situation_report.models import Statistic, Place


class Command(BaseCommand):

    def handle(self, *args, **options):

        # в бд добавляем статистику
        domain = 'https://www.worldometers.info'
        url = f'{domain}/coronavirus/#countries'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        table_tag = soup.find('div', class_="table-responsive")
        tbody_tag = table_tag.find('tbody')
        row = tbody_tag.find_all('tr')
        del (row[-1])
        for each in row:
            td_all = each.find_all('td')
            tag_number = 1
            for td_one in td_all:
                if tag_number == 1:
                    place = td_one.text.strip()
                    if not Place.objects.filter(place_name=place).exists():
                        if place != 'Total:':
                            Place.objects.create(place_name=place)
                        else:
                            break
                elif tag_number == 2:
                    total_cases = td_one.text
                elif tag_number == 3:
                    new_cases = td_one.text
                elif tag_number == 4:
                    total_death = td_one.text
                elif tag_number == 5:
                    new_death = td_one.text
                elif tag_number == 7:
                    total_recovered = td_one.text
                tag_number += 1

            today = datetime.today()
            if not Statistic.objects.filter(country_name=Place.objects.filter(
                    place_name=place).first(), date=today).exists():
                Statistic.objects.create(country_name=Place.objects.filter(
                    place_name=place).first(),
                                         date=today,
                                         total_cases=total_cases,
                                         new_cases=new_cases,
                                         total_deaths=total_death,
                                         new_deaths=new_death,
                                         total_recovered=total_recovered)

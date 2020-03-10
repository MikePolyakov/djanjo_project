from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from situation_report.models import Place, New, Statistic


class Command(BaseCommand):

    def handle(self, *args, **options):

        # в бд добавляем страны
        domain = 'https://www.who.int'
        url = f'{domain}/countries/en/'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        countries = soup.find('div', class_="col_1-1-1_1").find_all('span')
        for each in countries:
            if not Place.objects.filter(place_name=each.text).exists():
                Place.objects.create(place_name=each.text)

        # в бд добавляем новости
        domain = 'https://www.who.int'
        url = f'{domain}/emergencies/diseases/novel-coronavirus-2019/media-resources/news'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        first_tag = soup.find('div', class_="sf_colsIn col-md-10")
        info_tag = first_tag.find_all('div', class_="list-view")
        for each in info_tag:
            if not len(each.find('div', class_="info")) == 1:
                date_tag = each.find('p', class_="sub-title")
                date_str = str(date_tag)
                if date_str != 'None':
                    date_tag = date_tag.text
                    if date_tag[-1] == 'h':
                        date_tag = date_tag[:-9]
                    date = str(date_tag)
                    new_date = datetime.strptime(date, '%d %B %Y').date()
                else:
                    new_date = None

                title_tag = each.find('p', class_='heading text-underline').text
                a_tag = str(each.find('a', href=True)['href'])
                if not New.objects.filter(url=a_tag).exists():
                    New.objects.create(url=a_tag, date=new_date, name=title_tag)

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

from bs4 import BeautifulSoup
import requests
from datetime import datetime
from situation_report_app.models import Statistic, Place


def update():

    # обновляем статистику
    # be careful !!!
    Statistic.objects.all().delete()
    domain = 'https://www.worldometers.info'
    url = f'{domain}/coronavirus/#countries'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    print('page is opened')

    # table_tag = soup.find('div', class_="table-responsive")
    # tbody_tag = table_tag.find('tbody')
    tbody_tag = soup.find('tbody')
    row = tbody_tag.find_all('tr')

    country_added = 0
    for each in row:
        td_all = each.find_all('td')
        tag_number = 1
        for td_one in td_all:
            if tag_number == 1:
                place = td_one.text.strip()

                if not Place.objects.filter(place_name=place).exists():
                    if place != 'Total:':
                        Place.objects.create(place_name=place)
                        country_added += 1

            elif tag_number == 2:
                total_cases = td_one.text
            elif tag_number == 3:
                new_cases = td_one.text
            elif tag_number == 4:
                total_death = td_one.text
            elif tag_number == 5:
                new_death = td_one.text
            elif tag_number == 6:
                total_recovered = td_one.text
            tag_number += 1
        print(f'{place}, total cases {total_cases}')
        today = datetime.today()
        # if not Statistic.objects.filter(country_name=Place.objects.filter(
        #         place_name=place).first(), date=today).exists():
        Statistic.objects.create(country_name=Place.objects.filter(
             place_name=place).first(),
             date=today,
             total_cases=total_cases,
             new_cases=new_cases,
             total_deaths=total_death,
             new_deaths=new_death,
             total_recovered=total_recovered)
    total = Statistic.objects.all()

    print(f'{country_added} new countries added')
    print(f'total number of countries with COVID-19 = {len(total)}')

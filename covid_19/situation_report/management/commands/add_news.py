import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from situation_report.models import New
from datetime import datetime


class Command(BaseCommand):

    def handle(self, *args, **options):

        domain = 'https://www.who.int'
        url = f'{domain}/emergencies/diseases/novel-coronavirus-2019/media-resources/news'

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        first_tag = soup.find('div', class_="sf_colsIn col-md-10")
        info_tag = first_tag.find_all('div', class_="list-view")

        for each in info_tag:

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

            New.objects.create(url=a_tag, date=new_date, name=title_tag)

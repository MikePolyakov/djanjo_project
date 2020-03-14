from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from situation_report_app.models import Article


class Command(BaseCommand):

    def handle(self, *args, **options):

        # в бд добавляем новости
        domain = 'https://www.who.int'
        url = f'{domain}/emergencies/diseases/novel-coronavirus-2019/media-resources/news'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        first_tag = soup.find('div', class_="sf_colsIn col-md-10")
        info_tag = first_tag.find_all('div', class_="list-view")
        articles_added = 0
        for each in info_tag:
            if not len(each.find('div', class_="info")) == 1:
                date_tag = each.find('p', class_="sub-title")
                date_str = str(date_tag)
                if date_str != 'None':
                    date_tag = date_tag.text
                    symbol = 'I'
                    position = date_tag.find(symbol, 0)
                    if position != -1:
                        date_tag = date_tag[0:position-1]
                    date = str(date_tag)
                    new_date = datetime.strptime(date, '%d %B %Y').date()
                else:
                    new_date = None
                title_tag = each.find('p', class_='heading text-underline').text
                a_tag = str(each.find('a', href=True)['href'])
                if not Article.objects.filter(url=a_tag).exists():
                    Article.objects.create(url=a_tag, date=new_date, name=title_tag, source='World Health Organization')
                    articles_added += 1

        total_articles = Article.objects.all()

        print(f'added {articles_added}')
        print(f'total number of articles = {len(total_articles)}')

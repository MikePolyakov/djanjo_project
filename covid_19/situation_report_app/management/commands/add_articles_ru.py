from django.core.management.base import BaseCommand
from situation_report_app.models import Article, Source
from datetime import datetime
from tldextract import extract
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests


class Command(BaseCommand):

    def handle(self, *args, **options):

        # в бд добавляем новости
        domain = 'https://coronavirus-monitor.ru'
        url_news = f'{domain}/ru/novosti/?page='
        print(url_news)

        next_button = True
        print('Please wait... Start to get information...')
        page_counter = 1
        articles_added = 0
        i = 1

        while next_button:
            url = f'{url_news}{page_counter}'

            page_response = requests.get(url)
            page_soup = BeautifulSoup(page_response.text, 'html.parser')
            next_tag = page_soup.find('li', class_='next disabled')

            if next_tag is not None:
                next_button = False

            first_tag = page_soup.find("div", class_="p-about")
            articles = first_tag.find_all('div', class_="col-md-4 news-element")

            for each in articles:

                a_tag = each.find('a')
                href_url = a_tag.get('href')
                article_url = f'{domain}{href_url}'
                article_response = requests.get(article_url)
                article_soup = BeautifulSoup(article_response.text, 'html.parser')
                article_page = article_soup.find('div', class_='content')
                title = article_page.find('h1').text
                print(f'article # {i} (total will be limited to 12)')
                i += 1
                print(title)
                article_date = str(article_soup.find('span').text[0:10])
                date = datetime.strptime(article_date, '%d.%m.%Y').date()
                print(date)
                if article_soup.find('div', class_='col-md-8').find('a') is not None:

                    href_link = article_soup.find('div', class_='col-md-8').find('a').get('href')
                    print(href_link)

                if not Article.objects.filter(url=href_link).exists():
                    url_source = urlparse(href_link).netloc
                    tsd, td, tsu = extract(href_link)  # extracts abc, hostname, com
                    source = td + '.' + tsu  # joins as hostname.com
                    if not Source.objects.filter(url=url_source).exists():
                        Source.objects.create(name=source, url=url_source)

                    Article.objects.create(date=date,
                                           name=title,
                                           source=Source.objects.filter(url=url_source).first(),
                                           url=href_link)

                    articles_added += 1

            page_counter += 1

            # artificial limit 1page=12 articles
            # if page_counter > 1:
            #     next_button = False
            # artificial limit 1page=12 articles

        total_articles = Article.objects.all()
        print(f'added {articles_added}')
        print(f'total number of articles = {len(total_articles)}')

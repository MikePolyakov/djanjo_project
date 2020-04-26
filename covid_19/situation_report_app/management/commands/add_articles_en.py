from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from situation_report_app.models import Article, Source


class Command(BaseCommand):

    def handle(self, *args, **options):

        # в бд добавляем новости
        domain = 'https://www.who.int'
        url = f'{domain}/emergencies/diseases/novel-coronavirus-2019/media-resources/news'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        first_tag = soup.find("div", class_="sf_colsIn col-md-10")
        info_tag = first_tag.find_all('div', class_="list-view--item")
        # print(f'{len(info_tag)} articles were found')
        print("------------------------------------------------------")
        articles_added = 0
        for each in info_tag:

            if not len(each.find('div', class_="info")) == 1:

                date1_tag = each.find('span', class_="timestamp")
                # print(f'date1_tag {date1_tag} {type(date1_tag)}')
                if date1_tag != None:
                    # print("обработка tag1")
                    date = str(date1_tag.get_text(strip=True))
                    new_date = datetime.strptime(date, '%d %B %Y').date()
                    # print(f'new_date {new_date}')
                else:
                    # print("ищем tag2")
                    date2_tag = each.find('p', class_="sub-title")
                    date_str = str(date2_tag)
                    # print(f'date_str {date_str}')
                    if date_str != 'None':
                        date2_tag = date2_tag.text
                        year = '2020'
                        position = date2_tag.find(year, 0)
                        if position != -1:
                            date2_tag = date2_tag[0:position + 4]
                            # print(date2_tag)
                        date = str(date2_tag)
                        new_date = datetime.strptime(date, '%d %B %Y').date()
                    else:
                        new_date = None
                print(f'{new_date}')
                title_tag = each.find('p', class_='heading text-underline').text
                print(title_tag)
                a_tag = str(each.find('a', href=True)['href'])
                if not Article.objects.filter(url=a_tag).exists():
                    source = 'World Health Organization (WHO)'
                    if not Source.objects.filter(name=source).exists():
                        Source.objects.create(name=source, url='www.who.int')
                    Article.objects.create(url=a_tag,
                                           date=new_date,
                                           name=title_tag,
                                           source=Source.objects.filter(name=source).first())
                    articles_added += 1
            print("------------------------------------------------------")

        total_articles = Article.objects.all()

        print(f'added {articles_added}')
        print(f'total number of articles = {len(total_articles)}')

from django.core.management.base import BaseCommand
from situation_report_app.models import Article, Source
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
from datetime import datetime
from tldextract import extract
from urllib.parse import urlparse
from selenium.webdriver.chrome.options import Options


class Command(BaseCommand):

    def handle(self, *args, **options):

        # в бд добавляем новости
        domain = 'https://coronavirus-monitor.ru'
        url = f'{domain}/novosti/'

        try:
            options = Options()
            options.headless = True
            browser = webdriver.Chrome(chrome_options=options)
            browser.get(url)
            button_on_page = True
            click_counter = 1
            print('Please wait... Start to get information... Just a few clicks on button... Sorry :(')
            while button_on_page:
                button = browser.find_element_by_class_name("show-more.js-show-more-news")
                if button.is_displayed():
                    x = int(browser.find_element_by_class_name("show-more.js-show-more-news").location['x'])
                    y = int(browser.find_element_by_class_name("show-more.js-show-more-news").location['y'])
                    xy = browser.find_element_by_class_name("show-more.js-show-more-news").location

                    width = int(browser.find_element_by_class_name("show-more.js-show-more-news").size['width'])
                    height = int(browser.find_element_by_class_name("show-more.js-show-more-news").size['height'])

                    action = webdriver.common.action_chains.ActionChains(browser)
                    new_x = width / 2
                    new_y = height / 2

                    action.move_to_element_with_offset(button, new_x, new_y)
                    action.click()
                    action.perform()
                    time.sleep(1)
                    print(f'#{click_counter} click on button')
                    click_counter += 1

                else:
                    button_on_page = False

            article = browser.find_elements_by_class_name('article')
            i = 1
            articles_added = 0
            for each in article:
                title = each.find_element_by_class_name('title-article')
                date_tag = each.find_element_by_class_name('date')
                date = date_tag.text
                date = date[0:6]
                date = date + '2020'
                link = each.find_element_by_class_name('source')
                source = link.text
                href_link = link.get_attribute('href')
                print(href_link)
                print(i, date, source, title.text)
                i += 1
                date = str(date)
                new_date = datetime.strptime(date, '%d.%m.%Y').date()

                if not Article.objects.filter(url=href_link).exists():

                    if not Source.objects.filter(name=source).exists():
                        url = urlparse(href_link).netloc
                        # tsd, td, tsu = extract(href_link)  # extracts abc, hostname, com
                        # url = td + '.' + tsu  # joins as hostname.com
                        Source.objects.create(name=source, url=url)

                    Article.objects.create(date=new_date,
                                           name=title.text,
                                           source=Source.objects.filter(name=source).first(),
                                           url=href_link)

                    articles_added += 1

            total_articles = Article.objects.all()
            print(f'added {articles_added}')
            print(f'total number of articles = {len(total_articles)}')

        finally:
            # закрываем браузер после всех манипуляций
            browser.quit()



from situation_report_app.models import Article, Source
from selenium import webdriver
from datetime import datetime
from urllib.parse import urlparse
from selenium.webdriver.chrome.options import Options


def update_articles():

    # в бд добавляем новости
    domain = 'https://coronavirus-monitor.ru'
    url = f'{domain}/novosti/'

    try:
        options = Options()
        options.headless = True
        browser = webdriver.Chrome(chrome_options=options)
        browser.get(url)

        # article = browser.find_elements_by_class_name('article')
        article = browser.find_elements_by_class_name('row news')
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
                url_source = urlparse(href_link).netloc
                if not Source.objects.filter(url=url_source).exists():
                    Source.objects.create(name=source, url=url_source)

                Article.objects.create(date=new_date,
                                       name=title.text,
                                       source=Source.objects.filter(url=url_source).first(),
                                       url=href_link)

                articles_added += 1

        total_articles = Article.objects.all()
        print(type(total_articles))
        print(f'added {articles_added}')
        print(f'total number of articles = {len(total_articles)}')

    finally:
        # закрываем браузер после всех манипуляций
        browser.quit()

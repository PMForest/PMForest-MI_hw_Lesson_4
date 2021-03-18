'''Написать приложение, которое собирает основные новости с сайтов mail.ru, lenta.ru. Для парсинга использовать xpath. Структура данных должна содержать:

название источника,
наименование новости,
ссылку на новость,
дата публикации'''

from lxml import html
import requests
from datetime import datetime


def get_news_lenta_ru():
    news = []

    keys = ('title', 'date', 'link')
    date_format = '%Y-%m-%dT%H:%M:%S%z'
    link_lenta = 'https://lenta.ru/'

    request = requests.get(link_lenta)

    root = html.fromstring(request.text)
    root.make_links_absolute(link_lenta)

    news_links = root.xpath(
        '''//section//div[@class='span4 tondkc']//a'''
    )

    news_text = root.xpath(
        '''//section//div[@class='span4 tondkc']'''
    )

    for i in range(len(news_text)):
        news_text[i] = news_text[i].replace(u'\xa0', u' ')

    news_date = []

    for item in news_links:
        request = requests.get(item)
        root = html.fromstring(request.text)
        date = root.xpath("//section//div[@class='span4 tondkc']//a//time")
        news_date.extend(date)

    for i in range(len(news_date)):
        news_date[i] = datetime.strptime(news_date[i], date_format)

    for item in list(zip(news_text, news_date, news_links)):
        news_dict = {}
        for key, value in zip(keys, item):
            news_dict[key] = value

        news_dict['source'] = 'lenta.ru'
        news.append(news_dict)

    return news

print(get_news_lenta_ru())



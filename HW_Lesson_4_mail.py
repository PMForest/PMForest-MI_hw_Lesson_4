from lxml import html
import requests
from datetime import datetime

def get_news_mail_ru():

    news = []

    headers = {
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36' \
        '(KHTML, like Gecko) Chrome/88.0.4324.152 YaBrowser/21.2.3.100 Yowser/2.5 Safari/537.36'
    }

    keys = ('title', 'date', 'link')
    date_format = '%Y-%m-%dT%H:%M:%S%z'

    link_mail_ru = 'https://mail.ru/'

    request = requests.get(link_mail_ru, headers=headers)
    root = html.fromstring(request.text)

    news_links = root.xpath('''//div//tbody//tr//td//div//a''')

    news_text = root.xpath(
        '''//div//span//span[@class="photo__title photo__title_new photo__title_new_hidden js-topnews__notification"]'''
    )

    for i in range(len(news_text)):
        news_text[i] = news_text[i].replace(u'\xa0', u' ')

    news_links_temp = []
    for item in news_links:
        item = item.split('/')
        news_links_temp.append('/'.join(item[0:5]))

    news_links = news_links_temp
    del (news_links_temp)

    news_date = []

    for item in news_links:
        request = requests.get(item, headers=headers)
        root = html.fromstring(request.text)
        date = root.xpath(
            "//a[@class='photo photo_full photo_scale js-topnews__item']"
            "//img[@class='picture__image picture__image_cover photo__pic']"
                          )
        news_date.extend(date)

    for i in range(len(news_date)):
        news_date[i] = datetime.strptime(news_date[i], date_format)

    for item in list(zip(news_text, news_date, news_links)):
        news_dict = {}
        for key, value in zip(keys, item):
            news_dict[key] = value

        news_dict['source'] = 'mail.ru'
        news.append(news_dict)

    return news

print(get_news_mail_ru())
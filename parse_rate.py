import requests
from bs4 import BeautifulSoup
from datetime import datetime


def date_now():
    date = str(datetime.now().date())
    date = datetime.strptime(date, '%Y-%m-%d')
    return date.strftime('%d.%m.%Y')


def currency_on_day(date=date_now()):
    url = f'https://www.cbr.ru/currency_base/daily/?UniDbQuery.Posted=True&UniDbQuery.To={date}'
    headers = {
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Macintosh; PPC Mac OS X 10_7_0) AppleWebKit/5350 (KHTML, like Gecko) '
                      'Chrome/38.0.813.0 Mobile Safari/5350 '
    }

    req = requests.get(url, headers=headers)
    scr = req.text

    soup = BeautifulSoup(scr, 'lxml')

    return soup


def on_day_usd(date=date_now()):
    usd_on_day = currency_on_day(date).find(class_="data").find_all('td')
    for i in usd_on_day:
        if 'USD' in i:
            units = i.parent.find_all('td')[2].text
            usd_on_day = i.parent.find_all('td')[4].text
            return [usd_on_day, units]
    return 0


def print_usd(date=date_now()):
    cur_date = date_now()
    if \
            date[2:3] != '.' and date[5:6] != '.' \
            or len(date) > 10 \
            or 1992 > int(date[6:10]) \
            or int(date[6:10]) > int(cur_date[6:10]) \
            or (int(date[3:5]) < 7 and int(date[6:10]) == 1992) \
            or (int(date[6:10]) == int(cur_date[6:10]) and int(date[3:5]) > int(cur_date[3:5])) \
            or (int(date[6:10]) == int(cur_date[6:10]) and int(date[3:5]) == int(cur_date[3:5]) and int(
                date[0:2]) > int(cur_date[0:2])):
        return f'Данных по этой дате нет'
    temp = on_day_usd(date)
    if temp == 0:
        return f'Данных по этой дате нет'
    return f'Курс <b>USD</b> на {date} - <b>{temp[0]}</b> руб. за {temp[1]} USD'


def on_day_eur(date=datetime.now()):
    eur_on_day = currency_on_day(date).find(class_="data").find_all('td')
    for i in eur_on_day:
        if 'EUR' in i:
            units = i.parent.find_all('td')[2].text
            eur_on_day = i.parent.find_all('td')[4].text
            return [eur_on_day, units]
    return 0


def print_eur(date=date_now()):
    cur_date = date_now()
    if \
            date[2:3] != '.' and date[5:6] != '.' \
            or len(date) > 10 \
            or 1999 > int(date[6:10]) \
            or int(date[6:10]) > int(cur_date[6:10]) \
            or (int(date[3:5]) < 1 and int(date[6:10]) == 1999) \
            or (int(date[6:10]) == int(cur_date[6:10]) and int(date[3:5]) > int(cur_date[3:5])) \
            or (int(date[6:10]) == int(cur_date[6:10]) and int(date[3:5]) == int(cur_date[3:5]) and int(
                date[0:2]) > int(cur_date[0:2])):
        return f'Данных по этой дате нет'
    temp = on_day_eur()
    if temp == 0:
        return f'Данных по этой дате нет'
    return f'Курс <b>EUR</b> на {date} - <b>{temp[0]}</b> руб. за {temp[1]} EUR'

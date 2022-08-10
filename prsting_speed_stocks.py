import datetime
import json
import io

import requests  # для URL запроса
from bs4 import BeautifulSoup  # для работы с HTML
import time  # для установки задержки в цикле программы
box = {
    'header_link':{
        'adress': "https://ru.investing.com/equities/top-stock-gainers?country=russian_federation",
    },
    'gazp1' : {
        'adress': "https://www.google.com/finance/quote/GAZP:MCX?sa=X&ved=2ahUKEwjK5-z-yJLyAhUhpIsKHXbMBh0Q_AUoAXoECAEQAw",
        'class': "YMlKec fxKbKc"
    },
    'gazp' : {
        'adress': "https://ru.investing.com/equities/gazprom_rts",
        'class': "text-2xl",'data-test':'instrument-price-last'
    },
    'mmk' : {
        'adress': "https://ru.investing.com/equities/mmk_rts",
        'class': "text-2xl",'data-test':'instrument-price-last'
    },
    'sber' : {
        'adress': "https://ru.investing.com/equities/sberbank_rts",
        'class': "text-2xl','data-test':'instrument-price-last"
    }
}
sleep = 3  # время задержки

def anylis(adress):
    print(adress)
    headers = {
        'user agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/97.0.4692.99 Safari/537.36"}
    #html = requests.get(adress, headers)
    # парсим данные в переменную soup
    with open("header.html", encoding='utf-8') as f:
        src = f.read()
    #soup = BeautifulSoup(src, "lxml")
    soup = BeautifulSoup(src, 'html.parser')
    window = soup.find('table', {'class': 'genTbl closedTbl elpTbl elp25 crossRatesTbl'})
    spisok = window.find('tbody').find_all('tr')
    dict = {}
    for spisok1 in spisok:
        sp1_number_class = spisok1.find('td', {'class':'align_right'}).get('class')[1].split('-')[1]
        sp1_name = spisok1.find('td',{'class': 'left bold plusIconTd elp'}).find('a').text
        sp1_href = spisok1.find('td', {'class': 'left bold plusIconTd elp'}).find('a').get("href")
        sp1_price_last = spisok1.find('td', {'class': f'align_right pid-{sp1_number_class}-last'}).text
        sp1_price_max = spisok1.find('td',{'class': f'align_right pid-{sp1_number_class}-high'}).text
        sp1_price_min = spisok1.find('td',{'class': f'pid-{sp1_number_class}-low'}).text
        sp1_volume = spisok1.find('td',{'class': f'pid-{sp1_number_class}-turnover'}).text
        sp1_time_last = spisok1.find('td',{'class': f'pid-{sp1_number_class}-time'}).text
        #print(float(sp1_volume))
        if(sp1_volume[-1] == 'M'):
            dict[sp1_name] = {
                'href':sp1_href,
                'price_last':sp1_price_last,
                'price_max':sp1_price_max,
                'price_min':sp1_price_min,
                'volume':sp1_volume,
                'time':sp1_time_last
            }
            print("!!!!!", sp1_name, sp1_href, sp1_price_last, sp1_price_max, sp1_price_min, sp1_volume, sp1_number_class)
            print(len(dict))
            with open('test_data.json','w',encoding = 'utf-8') as f:
                json.dump(dict,f)
    #print(spisok1)
    window = soup.find('table', {'class': 'genTbl closedTbl elpTbl elp25 crossRatesTbl'})
    #spisok1 = soup.find("table")
    #print(spisok2)

anylis(box['header_link']['adress'])
def ticker(adress):

    # ссылка на тикер (Я использовал сайт google finance)
    #GAZP = "https://www.google.com/finance/quote/GAZP:MCX?sa=X&ved=2ahUKEwjK5-z-yJLyAhUhpIsKHXbMBh0Q_AUoAXoECAEQAw"
    # заголовки для URL запроса.(добавляется к ссылке при URL запросе)
    headers = {
        'user agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/97.0.4692.99 Safari/537.36"}
    # запрашиваем страницу по ссылке и помещаем в переменную html
    html = requests.get(adress, headers)
    # парсим данные в переменную soup
    soup = BeautifulSoup(html.content, 'html.parser')
    # находим интересующий нас тэг с текущей ценой акции
    # (В браузере используем просмотр кода элемента для того чтобы найти это значение)
    convert = soup.findAll('span', {'class': 'text-2xl','data-test':'instrument-price-last'})
    # считываем 1й элемент как текст.
    # Делаем срез и избавляемся от знака ₽ в начале строки,
    # конвертируем строку в число типа float
    price = convert[0].text

    # print("Цена акции Газпром: ", price)
    return price
    # time.sleep(sleep)
    # update_ticker_GAZP()  # вызываем эту же функцию снова


def update_ticker_GAZP():
    # ссылка на тикер (Я использовал сайт google finance)
    GAZP = "https://www.google.com/finance/quote/GAZP:MCX?sa=X&ved=2ahUKEwjK5-z-yJLyAhUhpIsKHXbMBh0Q_AUoAXoECAEQAw"
    # заголовки для URL запроса.(добавляется к ссылке при URL запросе)
    headers = {
    'user agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/97.0.4692.99 Safari/537.36"}
    # запрашиваем страницу по ссылке и помещаем в переменную html
    html = requests.get(GAZP, headers)
    # парсим данные в переменную soup
    soup = BeautifulSoup(html.content, 'html.parser')
    # находим интересующий нас тэг с текущей ценой акции
    # (В браузере используем просмотр кода элемента для того чтобы найти это значение)
    convert = soup.findAll('div', {'class': 'YMlKec fxKbKc'})
    # считываем 1й элемент как текст.
    # Делаем срез и избавляемся от знака ₽ в начале строки,
    # конвертируем строку в число типа float
    price = float(convert[0].text[1:])

    #print("Цена акции Газпром: ", price)
    return price
    #time.sleep(sleep)
    #update_ticker_GAZP()  # вызываем эту же функцию снова

def update_ticker_SBER():
    # ссылка на тикер (Я использовал сайт google finance)
    GAZP = "https://ru.investing.com/equities/sberbank_rts"
    # заголовки для URL запроса.(добавляется к ссылке при URL запросе)
    headers = {
        'user agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/97.0.4692.99 Safari/537.36"}
    # запрашиваем страницу по ссылке и помещаем в переменную html
    html = requests.get(GAZP, headers)
    # парсим данные в переменную soup
    soup = BeautifulSoup(html.content, 'html.parser')
    # находим интересующий нас тэг с текущей ценой акции
    # (В браузере используем просмотр кода элемента для того чтобы найти это значение)
    convert = soup.findAll('span', {'class': 'text-2xl','data-test':'instrument-price-last'})
    # считываем 1й элемент как текст.
    # Делаем срез и избавляемся от знака ₽ в начале строки,
    # конвертируем строку в число типа float
    ####price = float(convert[0].text[1:])
    price = convert[0].text
    #print("Цена акции SBER: ", price)
    return price
    #time.sleep(sleep)
    #test_SBER()  # вызываем эту же функцию снова
k = 0
"""if __name__ == '__main__':
    ticker_GAZP = {}
    ticker_SBER = {}
    while(True):
        time.sleep(sleep)

        #print("Цена акции Газпром: ", update_ticker_GAZP())
        #print("Цена акции SBER: ", update_ticker_SBER())
        #update_ticker_GAZP()
        print(datetime.datetime.today())
        ticker_GAZP [datetime.datetime.today()] = update_ticker_GAZP()
        ticker_SBER [datetime.datetime.today()] = update_ticker_SBER()
        #ticker ['SBER'] = update_ticker_SBER()



        d2 = {"id": 1948, "name": "Washer", "size": 3}
        with open('out.txt', 'w') as out:
            for key, val in d2.items():
                out.write('{}:{}\n'.format(key, val))
        with open('api.json','w') as f:
            f.write(ticker_GAZP)
            f.write(ticker_SBER)
"""
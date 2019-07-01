import ssl
import sys
import time
from datetime import datetime
from itertools import count
from urllib.request import Request, urlopen

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

from collection import crawler


def crawling_pelicana():
    results = []
    for page in count(start=1):
        url = f'https://pelicana.co.kr/store/stroe_search.html?page={page}&branch_name=&gu=&si='
        try:
            request = Request(url)
            ssl._create_default_https_context = ssl._create_unverified_context
            response = urlopen(request)

            receive = response.read()
            html = receive.decode('utf-8', errors='replace')
            # print(html)
            print(f'{datetime.now()}: success for request [{url}]')
        except Exception as e:
            print(f'{e} : {datetime.now()}', file=sys.stderr)
            continue

        # print(html)
        bs = BeautifulSoup(html, 'html.parser')
        tag_table = bs.find('table', attrs={'class': 'table mt20'})
        tag_tbody = tag_table.find('tbody')
        tags_tr = tag_tbody.findAll('tr')

        # 끝 검출
        if len(tags_tr) == 0:
            break
        for tag_tr in tags_tr:
            strings = list(tag_tr.strings)
            name = strings[1]
            addr = strings[3]
            sidogu = addr.split(' ')[:2]
            results.append((name, addr) + tuple(sidogu))

    # store
    table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gugun'])
    table.to_csv('__results__/pelicana.csv', encoding='utf-8', index=True)
    for t in results:
        print(t)


def crawloing_nene():
    results = []
    # for page in count(start=1): # for short test
    for page in range(1, 5):
        url = f'https://nenechicken.com/17_new/sub_shop01.asp?page={page}&ex_select=1&ex_select2=&IndexSword=&GUBUN=A'
        try:
            request = Request(url)
            ssl._create_default_https_context = ssl._create_unverified_context
            response = urlopen(request)

            receive = response.read()
            html = receive.decode('utf-8', errors='replace')
            # print(html)
            print(f'{datetime.now()}: success for request [{url}]')
        except Exception as e:
            print(f'{e} : {datetime.now()}', file=sys.stderr)

        bs = BeautifulSoup(html, 'html.parser')

        max_page = 0
        paging_div = bs.find('div', attrs={'class': 'pagination'})
        paging_divs = paging_div.findAll("a")
        for div in paging_divs:
            if div.text.isdigit():
                max_page = max(max_page, int(div.text))

        tag_table = bs.findAll('div', attrs={'class': 'shopInfo'})

        for tag in tag_table:
            shop_names = tag.find('div', attrs={'class': 'shopName'})
            shop_addrs = tag.find('div', attrs={'class': 'shopAdd'})
            results.append((shop_names.text, shop_addrs.text) + tuple(shop_addrs.text.split(' ')[:2]))

        if page >= max_page:
            break

    # store
    table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gugun'])
    table.to_csv('__results__/nene.csv', encoding='utf-8', index=True)
    for t in results:
        print(t)


def crawling_kyochon():
    results = []
    for sido1 in range(1, 18):
        for sido2 in count(start=1):
            url = 'http://www.kyochon.com/shop/domestic.asp?sido1=%d&sido2=%d&txtsearch=' % (sido1, sido2)
            html = crawler.crawling(url, encoding='utf-8')

            # 끝검출
            if html is None:
                break

            bs = BeautifulSoup(html, 'html.parser')
            tag_ul = bs.find('ul', attrs={'class': 'list'})
            tags_span = tag_ul.findAll('span', attrs={'class': 'store_item'})

            for tag_span in tags_span:
                strings = list(tag_span.strings)
                name = strings[1]
                address = strings[3].strip('\r\n\t')
                sidogu = address.split(' ')[:2]

                results.append((name, address) + tuple(sidogu))

    for t in results:
        print(t)

    # store
    table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gugun'])
    table.to_csv('__results__/kyochon.csv', encoding='utf-8', index=True)


def crawling_goobne():
    url = 'http://goobne.co.kr/store/search_store.jsp'

    wd = webdriver.Safari()
    wd.get(url)
    time.sleep(5)

    results = []

    for page in count(start=1):
        # 자바 스크립트 실행
        script = 'store.getList(%d)' % page
        wd.execute_script(script)
        print(f'{datetime.now} : success for request[{script}]')
        time.sleep(2)

        # 실행 결과 html 가져오기
        html = wd.page_source

        # parsing with bs4
        bs = BeautifulSoup(html, 'html.parser')
        tag_tbody = bs.find('tbody', attrs={'id': 'store_list'})
        tags_tr = tag_tbody.findAll('tr')

        # detect last page
        if tags_tr[0].get('class') is None:
            break

        for tag_tr in tags_tr:
            strings = list(tag_tr.strings)
            name = strings[1]
            address = strings[6]
            sidogu = address.split()[:2]
            results.append((name, address) + tuple(sidogu))

    wd.quit()

    for result in results:
        print(result)

    # store
    table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gugun'])
    table.to_csv('__results__/goobne.csv', encoding='utf-8', index=True)

if __name__ == '__main__':
    # crawling_pelicana()
    crawloing_nene()
    # crawling_kyochon()
    # crawling_goobne()

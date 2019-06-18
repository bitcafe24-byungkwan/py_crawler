import ssl
import sys
from datetime import datetime
from itertools import count
from urllib.request import Request, urlopen

import pandas as pd
from bs4 import BeautifulSoup


def crawling_pelicana():
    results = []
    for page in count(start=113):
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
    table.to_csv('__results__/pelicana.csv', encoding='utf-8', index = True)
    for t in results:
        print(t)


def crawloing_nene():
    pass


if __name__ == '__main__':
    crawling_pelicana()

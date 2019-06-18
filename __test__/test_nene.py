import ssl
import sys
from datetime import datetime
from itertools import count
from urllib.request import Request, urlopen

import pandas as pd
from bs4 import BeautifulSoup
results = []
for page in count(start=45):
    url = f'https://nenechicken.com/17_new/sub_shop01.asp?page={page}&ex_select=48&ex_select2=&IndexSword=&GUBUN=A'
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

    max_page = 0;
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

for res in results:
    print(res)





# # 끝 검출
# if len(tags_tr) == 0:
#     break
# for tag_tr in tags_tr:
#     strings = list(tag_tr.strings)
#     name = strings[1]
#     addr = strings[3]
#     sidogu = addr.split(' ')[:2]
#     results.append((name, addr) + tuple(sidogu))

# store
# table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gugun'])
# table.to_csv('__results__/pelicana.csv', encoding='utf-8', index = True)
# for t in results:
#     print(t)

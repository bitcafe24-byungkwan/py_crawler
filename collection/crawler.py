import ssl
import sys
from urllib.request import Request, urlopen
from datetime import datetime


def crawling(url='',
             encoding='utf-8',
             err=lambda e: print(f'{e} : {datetime.now()}', file=sys.stderr),
             proc1=lambda data: data,
             proc2=lambda data: data
             ):
    try:
        request = Request(url)
        ssl._create_default_https_context = ssl._create_unverified_context
        response = urlopen(request)

        print(f'{datetime.now()}: success for request [{url}]')

        receive = response.read()
        result = proc2(proc1(receive.decode(encoding, errors='replace')))

        return result
    except Exception as e:
        err(e)

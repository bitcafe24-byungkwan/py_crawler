import ssl
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

request = Request('https://movie.naver.com/movie/sdb/rank/rmovie.nhn')
ssl._create_default_https_context = ssl._create_unverified_context
response = urlopen(request)
html = response.read().decode('cp949')
print(html)

bs = BeautifulSoup(html, 'html.parser')
# print(bs.prettify())
divs = bs.findAll('div', attrs={'class': 'tit3'})

for index, div in enumerate(divs):
    print(index + 1, div.a.text, div.a['href'], sep=':')

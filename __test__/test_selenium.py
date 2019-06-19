import time
from selenium import webdriver

wd = webdriver.Safari()
wd.get('http://www.cafe24.com')

time.sleep(2)

html = wd.page_source
print(html)

wd.quit()

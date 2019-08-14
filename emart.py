from selenium import webdriver
import bs4
import sys
import io
import time

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

url = 'https://store.emart.com/branch/list.do?trcknCode=main_shop'

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable--gpu')
options.add_argument('–no-sandbox')
chromedriver_dir = r'chromedriver_ver/linux/chromedriver'
driver = webdriver.Chrome(chromedriver_dir, chrome_options=options)

driver.get(url)
time.sleep(3)
source = driver.page_source
driver.quit()
soup = bs4.BeautifulSoup(source, 'lxml')
stat = soup.find('div','sorting-bottom')
f = open('emart.txt', 'w')
day = stat.find_all('li','')

for i in day:
    title = i.find('a').text.strip()
    closed = i.find('span').text.strip()
    f.write('{} {}\n'.format(title, closed))
    
f.close()
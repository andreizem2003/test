# Web Scraping
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# Data manipulation
import pandas as pd
# Visualization
import matplotlib.pyplot as plt
import seaborn as sns
from sys import argv

webdriver_path = '../cromedriver/chromedriver.exe' # Enter the file directory of the Chromedriver
DNS_url = 'https://www.dns-shop.ru/'
if len(argv) == 1:
    search_item = "iphone 14"
else: 
    search_item = argv[1]
# Выберем нужные опции для запуска Chrome
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')
options.add_argument('--ignore-ssl-errors')
options.add_argument("--window-size=1920x1080")
options.add_argument('--headless') 
options.add_argument('start-maximized') 
options.add_argument('disable-infobars')
options.add_argument('--disable-extensions')
# Откроем браузер Chrome
browser = webdriver.Chrome(webdriver_path, options=options)
browser.get(DNS_url)

try:
    element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME,'q')))
finally:
    pass

search_bar = browser.find_element(By.NAME,'q')
search_bar.send_keys(search_item)
search_button = browser.find_element(By.CLASS_NAME,'presearch__icon-search')
search_button.click()

try:
    element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME,'presearch__icon-search')))
    element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME,'product-buy__price')))
finally:
    pass

item_titles = browser.find_elements(By.CLASS_NAME,'catalog-product__name')
item_prices = browser.find_elements(By.CLASS_NAME,'product-buy__price')


# Инициализируем пустые списки
titles_list = []
prices_list = []
# Наполним их названиями товаров и ценами
for title in item_titles:
    titles_list.append(title.text)
for price in item_prices:
    prices_list.append(price.text)
print(titles_list)
print(prices_list)
dfL = pd.DataFrame(zip(titles_list, prices_list), columns=['ItemName', 'Price'])
print(dfL)
dfL.to_csv(argv[0][0:-7] + "/demofile2.csv", sep="\t",encoding="utf-16")

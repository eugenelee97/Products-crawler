import time
import pandas as pd
import ssl
import sys
import urllib.request, json
from urllib.parse import urlparse
from selenium import webdriver
from bs4 import BeautifulSoup


ssl._create_default_https_context = ssl._create_unverified_context
response = urllib.request.urlopen('https://www.python.org')
headers = {'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}

# Command Line Passing Argument, python readURL.py keyword pagenumber
if len(sys.argv) < 3:
    sys.exit()
keyword = sys.argv[1]
pageNumber = int(sys.argv[2]) - 1

url = 'https://shopee.com.my/search?keyword={}&page={}&sortBy=relevancy'.format(keyword, pageNumber)

# Webdriver options
options = webdriver.ChromeOptions()
options.add_argument('disable-gpu')

driver = webdriver.Chrome('/Applications/chromedriver', options=options)
driver.get(url)
driver.implicitly_wait(5)

# Select language 
selectButton = driver.find_element_by_xpath("//*[@id='modal']/div[1]/div[1]/div/div[3]/div[1]/button")
selectButton.click()

# Declare array and time sleep to load website
product_list = []
time.sleep(1)

# Scroll down to load full website
SCROLL_PAUSE_TIME = 0.5
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(SCROLL_PAUSE_TIME)
    driver.execute_script("window.scrollTo(0, 1400);")
    time.sleep(SCROLL_PAUSE_TIME)
    driver.execute_script("window.scrollTo(0, 2200);")
    time.sleep(SCROLL_PAUSE_TIME)

    new_height = driver.execute_script("return document.body.scrollHeight")

    if new_height == last_height:
        break
    last_height = new_height

# Crawling website to get items
item_Class = driver.find_elements_by_css_selector("div.row.shopee-search-item-result__items > div > div> a")

for link in item_Class:

    # Url(url, picture url) of Items
    item_url = link.get_attribute("href")
    item_img = link.find_element_by_class_name("_1T9dHf.V1Fpl5").get_attribute("src").replace('_tn', '')
    
    # Split url to get item name, shop id, item id
    parts = urlparse(item_url)
    meta = parts.path.split('-i.')

    item_name = urllib.parse.unquote(meta[0].replace('/', '').replace('-', ' '))
    item_meta = meta[1].split('.')
    item_id = item_meta[1]

    shop_id = item_meta[0]  

    product_code = f'i.{meta[1]}'

     # Get seller name from Json Api
    with urllib.request.urlopen("https://shopee.com.my/api/v2/shop/get?is_brief=1&shopid={}".format(shop_id)) as url:
        data = json.loads(url.read().decode())
        seller_name = data['data']['account']['username']

    # Prices of Items
    item_prices = link.find_elements_by_class_name("_341bF0")
    if(len(item_prices) > 1):
        item_prices = f'{item_prices[0].text} - {item_prices[1].text}'
    else:
        item_prices = item_prices[0].text

    # Add all to product_list array
    product_list.append([item_name, item_prices, seller_name, item_url, product_code, f'=HYPERLINK(\"{item_img}\")'])

    # Send dataframe to csv
    df = pd.DataFrame(product_list, columns=['Product name', 'Prices', 'Seller Name', 'URL', 'Product Code', 'IMG'])
    df.to_csv(keyword + '_' + str(pageNumber) +'.csv', encoding="utf-8-sig")

 
driver.close()
driver.quit()
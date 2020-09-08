import pandas as pd
import sys
from selenium import webdriver

# Command Line Passing Argument. python checkURL.py csvfilename
if len(sys.argv) < 2:
    sys.exit()
filename = sys.argv[1]

# Dashboard URL lists, my = malaysia
groupware_url = 'https://ngwx.bizmeka.com/LoginN.aspx?compid=ipglobal'
my_searchbar_url = 'https://ngwx.bizmeka.com/myoffice/ezBoardSTD/SearchBoardItem_Cross.aspx?BoardID=%7B7e59b500-db26-80ee-ef14-82e9c0beac85%7D&OrgBoardParameters=Page%3D2%26BoardID%3D%7B7e59b500-db26-80ee-ef14-82e9c0beac85%7D%26SortBy%3D%26ListType%3D#'


# Read Product code from csv file
filepath = r'./' + filename + '.csv'
data = pd.read_csv(filepath, encoding = 'utf-8')
code = data["Product Code"]
code_list = code.values.tolist()

# Webdriver options
options = webdriver.ChromeOptions()
options.add_argument('disable-gpu')
options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36')

driver = webdriver.Chrome('/Applications/chromedriver', options=options)
driver.get(groupware_url)
driver.implicitly_wait(5)

# Automatic login
driver.find_element_by_name("TextUserID").send_keys("2007209123")
driver.find_element_by_name("TextPassword").send_keys("")

driver.find_element_by_xpath('//*[@id="LoginButton"]').click()

# Close popup window and switch to main window
main = driver.window_handles
for handle in main:
        if handle != main[0]:
            driver.switch_to.window(handle)
            driver.close()

driver.switch_to.window(main[0])

driver.get(my_searchbar_url)
driver.implicitly_wait(5)

for item in code_list :
    driver.find_element_by_id('txtTitle').clear()
    driver.find_element_by_id('txtTitle').send_keys(item)
    driver.find_element_by_xpath('/html/body/table[1]/tbody/tr[5]/td/a[2]/span').click()

    noresult = driver.find_element_by_css_selector('body > div:nth-child(8)').text

    if not (noresult):
        print(str(code_list.index(item)) + ' : ' + item + ' is already uploaded')

driver.close()
driver.quit()

  


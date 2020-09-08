import pandas as pd
import sys
from selenium import webdriver

# Command Line Passing Argument. python checkURL.py csvfilename
if len(sys.argv) < 2:
    sys.exit()
filename = sys.argv[1]

# Dashboard URL lists. my = malaysia
groupware_url = 'https://ngwx.bizmeka.com/LoginN.aspx?compid=ipglobal'
my_upload_url = 'https://ngwx.bizmeka.com/myoffice/ezBoardSTD/NewBoardItem_Cross.aspx?BoardID={7e59b500-db26-80ee-ef14-82e9c0beac85}&Mode=new&flag=N'

# Read Product code+url from csv file
filepath = r'./' + filename + '.csv'
data = pd.read_csv(filepath, encoding = 'utf-8')
item_url = data [["Product Code","URL"]]
item_url_list = item_url.values.tolist()

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

driver.get(my_upload_url)
driver.implicitly_wait(5)


for code,item in item_url_list:
    # Upload Posts, real xpath = //*[@id="menu"]/ul/li[1]/span
    driver.find_element_by_id("txtTitle").send_keys(code)
    driver.switch_to.frame("message") 
    driver.find_element_by_xpath("/html/body/div[1]/div[4]/ul/li[2]/a/span").click()
    driver.find_element_by_class_name("kk_htmlContents").clear()
    driver.find_element_by_class_name("kk_htmlContents").send_keys(item)
    driver.switch_to.default_content()
    driver.find_element_by_xpath('//*[@id="temp_board"]/span').click()
    # Close Alert
    alert = driver.switch_to.alert
    alert.accept()

driver.close()
driver.quit()




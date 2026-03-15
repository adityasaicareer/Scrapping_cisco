from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

mgurl = "https://documentation.meraki.com/SASE_and_SD-WAN/Cellular/Product_Information/Overviews_and_Datasheets"

driver.get(mgurl)
# driver have the webpage

# title = driver.find_element(By.ID, "title")
# title = title.text
# print(title)


"""
Links of products
"""

"""
driver - we have complete webpage

find_element/tags

two methods finding elements in driver

1.find_element- first match
2.find_elements- all matches(list)

"""

mglinks = driver.find_elements(By.CSS_SELECTOR, ".mt-listings-simple li")
# css classes
# . for class names
# # for id
#


print(len(mglinks))

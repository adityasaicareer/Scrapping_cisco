from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url="https://documentation.meraki.com/Switching/MS_-_Switches/Product_Information/Overviews_and_Datasheets"
options=Options()

options.add_argument("--headless")
# options.add_argument("--start-maximized")

driver=webdriver.Chrome(options=options)

driver.get(url)
wait=WebDriverWait(driver,5)

elements=driver.find_elements(By.CSS_SELECTOR,"ul.mt-listings-simple > li")
print(elements)

parseurls=[]

for element in elements:
  anchor=element.find_element(By.TAG_NAME,"a")
  href=anchor.get_attribute("href")
  print(href)
  parseurls.append(href)
print(parseurls)






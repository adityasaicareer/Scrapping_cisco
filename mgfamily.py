from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import json

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

mglinks = driver.find_elements(By.CSS_SELECTOR, ".mt-listings-simple li a")
# css classes
# . for class names
# # for id
#

links=[link.get_attribute("href") for link in mglinks]
print(links)
print(len(mglinks))

output=[]
for link in links:
  tempdir={}
  tempdir["family"]="MG"
  tempdir["link"]=link
  tempdriver=webdriver.Chrome(options=options)

  tempdriver.get(link)
  tempdir["title"]=tempdriver.find_element(By.CSS_SELECTOR,"#title").text
  print(tempdir)
  tempdir["overview"]=tempdriver.find_elements(By.CSS_SELECTOR,"p")[2].text
  tempdir["features"]= [feature.text for feature in tempdriver.find_elements(By.CSS_SELECTOR,"#section_2 ul li strong")]

  output.append(tempdir)
print(output)

with open("/Users/chowdaryadithyasai/scrapping/output.json",'r') as f:
    data=json.load(f)

data.append(output)
with open("/Users/chowdaryadithyasai/scrapping/output.json",'w') as f:
    json.dump(data,f,indent=4)
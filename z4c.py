from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

options = Options()
options.add_argument("--headless")


driver = webdriver.Chrome(options=options)
WebDriverWait(driver, 3)

zurl = "https://documentation.meraki.com/SASE_and_SD-WAN/Z-Series_Teleworker_Gateways/Product_Information/Z4C_Datasheet"


subdriver = webdriver.Chrome(options=options)
subdriver.get(zurl)
WebDriverWait(subdriver, 3)

title = subdriver.find_element(By.ID, "title")
title = title.text
title = title.split(" ")[0]
tempdir={}
tempdir["title"] = title

overview = subdriver.find_elements(By.CSS_SELECTOR, "#section_1 p")
print(overview)
overviewtext = ""
for over in overview:
    overviewtext += over.text

tempdir["overview"] = overviewtext

tempdir['link']=zurl

features1=subdriver.find_elements(By.CSS_SELECTOR, "#section_3 ul")
features=[]
for i in features1:
    print(i.text)
    features.append(i.text)
features2=subdriver.find_elements(By.CSS_SELECTOR, "#section_4 ul")
for i in features2:
    features.append(i.text)
tempdir['features']=features
print(tempdir)


import json

with open("/Users/chowdaryadithyasai/scrapping/output.json",'r') as f:
    data=json.load(f)

data.append(tempdir)
with open("/Users/chowdaryadithyasai/scrapping/output.json",'w') as f:
    json.dump(data,f,indent=4)
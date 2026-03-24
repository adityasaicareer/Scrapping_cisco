from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

options = Options()
options.add_argument("--headless")


driver = webdriver.Chrome(options=options)
WebDriverWait(driver, 3)

mxurl = "https://documentation.meraki.com/SASE_and_SD-WAN/MX/Product_Information/Overviews_and_Datasheets"

driver.get(mxurl)
WebDriverWait(driver, 3)

listing = driver.find_elements(By.CSS_SELECTOR, ".mt-listing-no-break")
print(len(listing))
mxfamily = listing[1]


mxlist = mxfamily.find_elements(By.CSS_SELECTOR, "ul li")
print(len(mxlist))
mxoutput = []
for mx in mxlist:
    anchor = mx.find_element(By.TAG_NAME, "a")
    link = anchor.get_attribute("href")
    tempdir = {}
    tempdir["family"] = "MX"
    tempdir["link"] = link

    subdriver = webdriver.Chrome(options=options)
    subdriver.get(link)
    WebDriverWait(subdriver, 3)

    title = subdriver.find_element(By.ID, "title")
    title = title.text
    title = title.split(" ")[0]
    tempdir["title"] = title

    overview = subdriver.find_elements(By.CSS_SELECTOR, "#section_1 p")
    overview = overview[:-3]
    overviewtext = ""
    for over in overview:
        overviewtext += over.text

    tempdir["overview"] = overviewtext
    print(tempdir)

import json

with open("outupt.json",'r') as f:
    data=json.load(f)
data.append(tempdir)
with open("output.json",'w') as f:
    json.dump(data,f,indent=4)
    
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

options = Options()
options.add_argument("--headless")


driver = webdriver.Chrome(options=options)
WebDriverWait(driver, 3)

caturl = "https://documentation.meraki.com/Switching/Cloud_Management_with_IOS_XE/Product_Information/Overviews_and_Datasheets"

driver.get(caturl)
WebDriverWait(driver, 3)

listing = driver.find_elements(By.CSS_SELECTOR, ".mt-listing-no-break ul")
print(len(listing))
catfamily = listing[0]


catlist = catfamily.find_elements(By.CSS_SELECTOR, "ul li")
print(len(catlist))
cat = []
for c in catlist:
    anchor = c.find_element(By.TAG_NAME, "a")
    link = anchor.get_attribute("href")
    tempdir = {}
    tempdir["family"] = "C"
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
    cat.append(tempdir)
import json

with open("/Users/chowdaryadithyasai/scrapping/output.json",'r') as f:
    data=json.load(f)

data.append(cat)
with open("/Users/chowdaryadithyasai/scrapping/output.json",'w') as f:
    json.dump(data,f,indent=4)
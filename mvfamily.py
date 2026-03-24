from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

mvurl = "https://documentation.meraki.com/IoT/MV_-_Smart_Cameras/Product_Information"

options = Options()

options.add_argument("--headless")

driver = webdriver.Chrome(options=options)
driver.get(mvurl)
WebDriverWait(driver, 2)

listofmv = driver.find_element(By.CSS_SELECTOR, ".mt-reveal-listing")
list = listofmv.find_elements(By.TAG_NAME, "li")

mvlinks = []
list = list[:-3]

mvoutput = []

for mv in list:
    anchor = mv.find_element(By.TAG_NAME, "a")
    link = anchor.get_attribute("href")
    tempdir = {}
    tempdir["link"] = link
    tempdir["family"] = "MV"
    subdriver = webdriver.Chrome(options=options)
    subdriver.get(link)
    WebDriverWait(subdriver, 3)

    title = subdriver.find_element(By.ID, "title")
    title = title.text
    title = title.split(" ")
    title = title[0]
    tempdir["title"] = title

    overview = subdriver.find_element(By.CSS_SELECTOR, "#section_1 p")
    overview = overview.text
    tempdir["overview"] = overview

    features = subdriver.find_element(By.CSS_SELECTOR, "table")
    features = features.find_elements(By.CSS_SELECTOR, "tbody tr td ul li")
    tempfeatures = []
    for feature in features:
        f = feature.text
        tempfeatures.append(f)
    tempdir["features"] = tempfeatures
    print(tempdir)
    mvoutput.append(tempdir)


print(mvoutput)



import json

with open("/Users/chowdaryadithyasai/scrapping/output.json",'r') as f:
    data=json.load(f)

data.append(mvoutput)
with open("/Users/chowdaryadithyasai/scrapping/output.json",'w') as f:
    json.dump(data,f,indent=4)
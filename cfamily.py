from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

options = Options()
options.add_argument("--headless")


driver = webdriver.Chrome(options=options)
WebDriverWait(driver, 3)

curl = "https://documentation.meraki.com/Wireless/Product_Information/Overviews_and_Datasheets"

driver.get(curl)
WebDriverWait(driver, 3)

listing = driver.find_elements(By.CSS_SELECTOR, ".mt-listings-simple")
print(len(listing))
cfamily = listing[0]


clist = cfamily.find_elements(By.CSS_SELECTOR, "ul li")
print(len(clist))
mxoutput = []
for c in clist:
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

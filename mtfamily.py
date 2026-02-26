from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

options = Options()
options.add_argument("--headless")

driver = webdriver.Chrome(options=options)

mturl = "https://documentation.meraki.com/IoT/MT_-_Sensors/Product_Information"
print(mturl)
mtoutput = []

driver.get(mturl)
WebDriverWait(driver, 3)

mturls = driver.find_element(By.CSS_SELECTOR, ".mt-reveal-listing")
mturls = mturls.find_elements(By.TAG_NAME, "li")
mturls = mturls[:-2]
print(len(mturls))
for mturl in mturls:
    anchor = mturl.find_element(By.TAG_NAME, "a")
    link = anchor.get_attribute("href")
    tempdir = {}
    print(link)
    tempdir["link"] = link
    tempdir["family"] = "MT"

    subdriver = webdriver.Chrome(options=options)

    subdriver.get(link)
    WebDriverWait(subdriver, 3)

    title = subdriver.find_element(By.ID, "title").text
    title = title.split(" ")
    title = title[0]
    tempdir["title"] = title

    overview = subdriver.find_element(By.CSS_SELECTOR, "#section_2")
    overview = overview.find_elements(By.TAG_NAME, "p")
    overviewtext = ""
    for over in overview:
        overviewtext += over.text

    tempdict["overview"] = overviewtext
    print(tempdict)

    mtoutput.append(tempdir)

    subdriver.quit()

print(mtoutput)

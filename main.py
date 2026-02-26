from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

url = "https://documentation.meraki.com/Switching/MS_-_Switches/Product_Information/Overviews_and_Datasheets"
options = Options()

options.add_argument("--headless")
# options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)

driver.get(url)
wait = WebDriverWait(driver, 5)

elements = driver.find_elements(By.CSS_SELECTOR, "ul.mt-listings-simple > li")
print(elements)

parseurls = []

for element in elements:
    anchor = element.find_element(By.TAG_NAME, "a")
    href = anchor.get_attribute("href")
    print(href)
    parseurls.append(href)
print(parseurls)


options = Options()
options.add_argument("--headless")


print(parseurls)
output = []
for url in parseurls:
    tempdict = {}
    tempdict["family"] = "MS"
    subdrive = webdriver.Chrome(options=options)
    subdrive.get(url)
    tempdict["url"] = url

    titleelement = subdrive.find_element(By.ID, "title")
    title = titleelement.text
    titles = title.split(" ")
    title = titles[0]

    tempdict["title"] = title

    overview = subdrive.find_elements(By.CSS_SELECTOR, "#section_1 p")
    tempdict["overview"] = overview[1].text + "\n" + overview[2].text

    features = subdrive.find_elements(By.CSS_SELECTOR, "#section_2 table tr td")
    featurelist = []
    for feature in features:
        l1 = feature.find_elements(By.CSS_SELECTOR, "ul li")
        for l in l1:
            featurelist.append(l.text)
    tempdict["features"] = featurelist
    print(tempdict)
    output.append(tempdict)

driver.quit()
# Mr and cw family

mrcw = "https://documentation.meraki.com/Wireless/Product_Information/Overviews_and_Datasheets"
driver = webdriver.Chrome(options=options)
driver.get(mrcw)
WebDriverWait(driver, 3)

elements = driver.find_elements(By.CSS_SELECTOR, ".mt-listing-no-break")
cwelements = elements[0]
mrfamily = elements[2]
cwelements = cwelements.find_elements(By.CSS_SELECTOR, ".mt-listings-simple li")
mrfamily = mrfamily.find_elements(By.CSS_SELECTOR, ".mt-listings-simple li")
print(f"cw elements {len(cwelements)}")
print(f"mr family list {len(mrfamily)}")

cwurls = []
mrurls = []
for cw in cwelements:
    anchor = cw.find_element(By.TAG_NAME, "a")
    link = anchor.get_attribute("href")
    print(link)
    cwurls.append(link)

cwurls = cwurls[2:]

for mr in mrfamily:
    anchor = mr.find_element(By.TAG_NAME, "a")
    link = anchor.get_attribute("href")
    print(link)
    mrurls.append(link)

mradditional = driver.find_elements(By.CSS_SELECTOR, "#section_1 p")
print(len(mrurls))
for mr in mradditional:
    anchor = mr.find_element(By.TAG_NAME, "a")
    print(anchor.text)
    link = anchor.get_attribute("href")
    print(link)
    mrurls.append(link)

print(len(mrurls))

for cw in cwurls:
    print(cw)
    subdriver = webdriver.Chrome(options=options)
    tempdir = {}
    subdriver.get(cw)
    WebDriverWait(subdriver, 5)
    title = subdriver.find_element(By.ID, "title").text
    title = title.split(" ")
    title = title[0]
    print(title)
    tempdir["family"] = "CW"
    tempdir["title"] = title
    try:
        description = subdriver.find_element(By.CSS_SELECTOR, "#section_1 h2")
        description = description.text
        tempdir["description"] = description
    except:
        tempdir["description"] = ""
    try:
        overview = subdriver.find_element(By.CSS_SELECTOR, "#section_1 p")
        overview = overview.text
        print(description)
        print(overview)
        tempdir["overview"] = overview
    except:
        tempdir["overview"] = ""

    try:
        features_table = subdriver.find_element(By.TAG_NAME, "table")
        features = features_table.find_elements(By.CSS_SELECTOR, "tbody tr td ul li")

        print(len(features))
        featurelist = []
        for feature in features:
            featurelist.append(feature.text)
        tempdir["feature"] = featurelist
    except:
        tempdir["feature"] = []

    output.append(tempdir)

    print(tempdir)


mrurls = mrurls[2:]

for mr in mrurls:
    print(mr)
    subdriver = webdriver.Chrome(options=options)
    tempdir = {}
    subdriver.get(mr)
    WebDriverWait(subdriver, 5)
    title = subdriver.find_element(By.ID, "title").text
    title = title.split(" ")
    title = title[0]
    print(title)
    tempdir["family"] = "MR"
    tempdir["title"] = title
    try:
        description = subdriver.find_element(By.CSS_SELECTOR, "#section_1 h3")
        description = description.text
        tempdir["description"] = description
    except:
        tempdir["description"] = ""
    try:
        overview = subdriver.find_elements(By.CSS_SELECTOR, "#section_1 p")
        overviewtext = ""
        for i in overview:
            overviewtext = i.text + "\n\n"
        overview = overviewtext
        print(description)
        print(overview)
        tempdir["overview"] = overview
    except:
        tempdir["overview"] = ""

    try:
        features_table = subdriver.find_element(By.TAG_NAME, "table")
        features = features_table.find_elements(By.CSS_SELECTOR, "tbody tr td ul li")

        print(len(features))
        featurelist = []
        for feature in features:
            featurelist.append(feature.text)
        tempdir["feature"] = featurelist
    except:
        tempdir["feature"] = []

    output.append(tempdir)

    print(tempdir)


driver.quit()

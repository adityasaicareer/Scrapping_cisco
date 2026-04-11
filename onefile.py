from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import json
import os

# ── Chrome options ──────────────────────────────────────────────────────────
options = Options()
options.add_argument("--headless")

OUTPUT_FILE = "output.json"

# ── Helper: load / initialise output file ───────────────────────────────────
def load_output():
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r") as f:
            return json.load(f)
    return []

def save_output(data):
    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=4)


# ── 1. MX Family ─────────────────────────────────────────────────────────────
def scrape_mx():
    print("\n=== Scraping MX Family ===")
    mxurl = "https://documentation.meraki.com/SASE_and_SD-WAN/MX/Product_Information/Overviews_and_Datasheets"
    driver = webdriver.Chrome(options=options)
    driver.get(mxurl)
    WebDriverWait(driver, 3)

    listing = driver.find_elements(By.CSS_SELECTOR, ".mt-listing-no-break")
    mxfamily = listing[1]
    mxlist = mxfamily.find_elements(By.CSS_SELECTOR, "ul li")
    print(f"MX products found: {len(mxlist)}")

    mxoutput = []
    for mx in mxlist:
        anchor = mx.find_element(By.TAG_NAME, "a")
        link = anchor.get_attribute("href")
        tempdir = {"family": "MX", "link": link}

        subdriver = webdriver.Chrome(options=options)
        subdriver.get(link)
        WebDriverWait(subdriver, 3)

        title = subdriver.find_element(By.ID, "title").text.split(" ")[0]
        tempdir["title"] = title

        overview_els = subdriver.find_elements(By.CSS_SELECTOR, "#section_1 p")[:-3]
        tempdir["overview"] = "".join(el.text for el in overview_els)

        print(tempdir)
        mxoutput.append(tempdir)
        subdriver.quit()

    driver.quit()
    return mxoutput


# ── 2. MV Family (Smart Cameras) ─────────────────────────────────────────────
def scrape_mv():
    print("\n=== Scraping MV Family ===")
    mvurl = "https://documentation.meraki.com/IoT/MV_-_Smart_Cameras/Product_Information"
    driver = webdriver.Chrome(options=options)
    driver.get(mvurl)
    WebDriverWait(driver, 2)

    listofmv = driver.find_element(By.CSS_SELECTOR, ".mt-reveal-listing")
    items = listofmv.find_elements(By.TAG_NAME, "li")[:-3]
    print(f"MV products found: {len(items)}")

    mvoutput = []
    for mv in items:
        anchor = mv.find_element(By.TAG_NAME, "a")
        link = anchor.get_attribute("href")
        tempdir = {"link": link, "family": "MV"}

        subdriver = webdriver.Chrome(options=options)
        subdriver.get(link)
        WebDriverWait(subdriver, 3)

        title = subdriver.find_element(By.ID, "title").text.split(" ")[0]
        tempdir["title"] = title
        tempdir["overview"] = subdriver.find_element(By.CSS_SELECTOR, "#section_1 p").text

        features_els = subdriver.find_elements(By.CSS_SELECTOR, "table tbody tr td ul li")
        tempdir["features"] = [f.text for f in features_els]

        print(tempdir)
        mvoutput.append(tempdir)
        subdriver.quit()

    driver.quit()
    return mvoutput


# ── 3. MT Family (Sensors) ───────────────────────────────────────────────────
def scrape_mt():
    print("\n=== Scraping MT Family ===")
    mturl = "https://documentation.meraki.com/IoT/MT_-_Sensors/Product_Information"
    driver = webdriver.Chrome(options=options)
    driver.get(mturl)
    WebDriverWait(driver, 3)

    mturls = driver.find_element(By.CSS_SELECTOR, ".mt-reveal-listing")
    items = mturls.find_elements(By.TAG_NAME, "li")[:-2]
    print(f"MT products found: {len(items)}")

    mtoutput = []
    for item in items:
        anchor = item.find_element(By.TAG_NAME, "a")
        link = anchor.get_attribute("href")
        tempdir = {"link": link, "family": "MT"}

        subdriver = webdriver.Chrome(options=options)
        subdriver.get(link)
        WebDriverWait(subdriver, 3)

        title = subdriver.find_element(By.ID, "title").text.split(" ")[0]
        tempdir["title"] = title

        overview_els = subdriver.find_element(By.CSS_SELECTOR, "#section_2").find_elements(By.TAG_NAME, "p")
        tempdir["overview"] = "".join(el.text for el in overview_els)

        print(tempdir)
        mtoutput.append(tempdir)
        subdriver.quit()

    driver.quit()
    return mtoutput


# ── 4. MG Family (Cellular) ──────────────────────────────────────────────────
def scrape_mg():
    print("\n=== Scraping MG Family ===")
    mgurl = "https://documentation.meraki.com/SASE_and_SD-WAN/Cellular/Product_Information/Overviews_and_Datasheets"
    driver = webdriver.Chrome(options=options)
    driver.get(mgurl)

    mglinks = driver.find_elements(By.CSS_SELECTOR, ".mt-listings-simple li a")
    links = [link.get_attribute("href") for link in mglinks]
    print(f"MG products found: {len(links)}")

    output = []
    for link in links:
        tempdir = {"family": "MG", "link": link}

        tempdriver = webdriver.Chrome(options=options)
        tempdriver.get(link)

        tempdir["title"] = tempdriver.find_element(By.CSS_SELECTOR, "#title").text
        tempdir["overview"] = tempdriver.find_elements(By.CSS_SELECTOR, "p")[2].text
        tempdir["features"] = [
            f.text for f in tempdriver.find_elements(By.CSS_SELECTOR, "#section_2 ul li strong")
        ]

        print(tempdir)
        output.append(tempdir)
        tempdriver.quit()

    driver.quit()
    return output


# ── 5. C Family (Wireless) ───────────────────────────────────────────────────
def scrape_c():
    print("\n=== Scraping C Family ===")
    curl = "https://documentation.meraki.com/Wireless/Product_Information/Overviews_and_Datasheets"
    driver = webdriver.Chrome(options=options)
    driver.get(curl)
    WebDriverWait(driver, 3)

    listing = driver.find_elements(By.CSS_SELECTOR, ".mt-listings-simple")
    cfamily = listing[0]
    clist = cfamily.find_elements(By.CSS_SELECTOR, "ul li")
    print(f"C (Wireless) products found: {len(clist)}")

    coutput = []
    for c in clist:
        anchor = c.find_element(By.TAG_NAME, "a")
        link = anchor.get_attribute("href")
        tempdir = {"family": "C", "link": link}

        subdriver = webdriver.Chrome(options=options)
        subdriver.get(link)
        WebDriverWait(subdriver, 3)

        title = subdriver.find_element(By.ID, "title").text.split(" ")[0]
        tempdir["title"] = title

        overview_els = subdriver.find_elements(By.CSS_SELECTOR, "#section_1 p")[:-3]
        tempdir["overview"] = "".join(el.text for el in overview_els)

        print(tempdir)
        coutput.append(tempdir)
        subdriver.quit()

    driver.quit()
    return coutput


# ── 6. Catalyst / IOS-XE Switching ───────────────────────────────────────────
def scrape_catalyst():
    print("\n=== Scraping Catalyst (IOS-XE) Family ===")
    caturl = "https://documentation.meraki.com/Switching/Cloud_Management_with_IOS_XE/Product_Information/Overviews_and_Datasheets"
    driver = webdriver.Chrome(options=options)
    driver.get(caturl)
    WebDriverWait(driver, 3)

    listing = driver.find_elements(By.CSS_SELECTOR, ".mt-listing-no-break ul")
    catfamily = listing[0]
    catlist = catfamily.find_elements(By.CSS_SELECTOR, "ul li")
    print(f"Catalyst products found: {len(catlist)}")

    cat = []
    for c in catlist:
        anchor = c.find_element(By.TAG_NAME, "a")
        link = anchor.get_attribute("href")
        tempdir = {"family": "C", "link": link}

        subdriver = webdriver.Chrome(options=options)
        subdriver.get(link)
        WebDriverWait(subdriver, 3)

        title = subdriver.find_element(By.ID, "title").text.split(" ")[0]
        tempdir["title"] = title

        overview_els = subdriver.find_elements(By.CSS_SELECTOR, "#section_1 p")[:-3]
        tempdir["overview"] = "".join(el.text for el in overview_els)

        print(tempdir)
        cat.append(tempdir)
        subdriver.quit()

    driver.quit()
    return cat


# ── 7. Z4C (Teleworker Gateway) ──────────────────────────────────────────────
def scrape_z4c():
    print("\n=== Scraping Z4C ===")
    zurl = "https://documentation.meraki.com/SASE_and_SD-WAN/Z-Series_Teleworker_Gateways/Product_Information/Z4C_Datasheet"

    subdriver = webdriver.Chrome(options=options)
    subdriver.get(zurl)
    WebDriverWait(subdriver, 3)

    tempdir = {}
    tempdir["title"] = subdriver.find_element(By.ID, "title").text.split(" ")[0]
    tempdir["family"] = "Z"
    tempdir["link"] = zurl

    overview_els = subdriver.find_elements(By.CSS_SELECTOR, "#section_1 p")
    tempdir["overview"] = "".join(el.text for el in overview_els)

    features = []
    for el in subdriver.find_elements(By.CSS_SELECTOR, "#section_3 ul"):
        features.append(el.text)
    for el in subdriver.find_elements(By.CSS_SELECTOR, "#section_4 ul"):
        features.append(el.text)
    tempdir["features"] = features

    print(tempdir)
    subdriver.quit()
    return [tempdir]   # wrap in list for uniform handling


# ── Main ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    data = load_output()

    scrapers = [
        scrape_mx,
        scrape_mv,
        scrape_mt,
        scrape_mg,
        scrape_c,
        scrape_catalyst,
        scrape_z4c,
    ]

    for scraper in scrapers:
        try:
            result = scraper()
            data.append(result)
            save_output(data)          # save after each family so progress isn't lost
            print(f"  ✓ Saved {len(result)} records from {scraper.__name__}")
        except Exception as e:
            print(f"  ✗ {scraper.__name__} failed: {e}")

    print(f"\nDone! Total groups in output.json: {len(data)}")
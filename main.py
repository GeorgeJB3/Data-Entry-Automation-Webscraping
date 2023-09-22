from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import requests

CHROME_DRIVER_PATH = "/Users/georgebaldwin/Development/chromedriver"
CHROME_OPTIONS = webdriver.ChromeOptions()
CHROME_OPTIONS.add_experimental_option("detach", True)

FORM_LINK = 'https://docs.google.com/forms/d/e/1FAIpQLSczLg6irA2mAuBK6n72shjXq8tNDzKHPcE4ts6V8AJtDolC3A/viewform?usp=sf_link'
ZILLOW = "https://www.zillow.com/san-francisco-ca/rentals/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22north%22%3A37.85137173926443%2C%22east%22%3A-122.31488314990234%2C%22south%22%3A37.69913379718079%2C%22west%22%3A-122.55177585009766%7D%2C%22mapZoom%22%3A12%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%7D"
FORM_RESPONSE = 'https://docs.google.com/forms/d/1vEFhV9swuLet55WsC9Yfmd71yVDmx7AlhQtC0ixh5bg/edit?pli=1#responses'
EMAIL = "pythontest401@gmail.com"


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
                  "(KHTML, like Gecko) Version/15.6.1 Safari/605.1.15",
    "Accept-Language": "en-GB,en;q=0.9"
}

response = requests.get(url=ZILLOW, headers=HEADERS)
properties = response.text
soup = BeautifulSoup(properties, "html.parser")

# Scrapes prices, addresses and links from Zillow
all_prices = soup.select('span[data-test="property-card-price"]')
all_addresses = soup.select('address[data-test="property-card-addr"]')
all_links = soup.select('a[class="Anchor-c11n-8-84-3__sc-hn4bge-0 kxrUt carousel-photo"]')

address = [address.getText() for address in all_addresses]
price = [price.getText().split(' ')[0] for price in all_prices]
half_link = [link.get("href") for link in all_links]
complete_link = [f"https://www.zillow.com{part}" for part in half_link]

driver = webdriver.Chrome(CHROME_OPTIONS)
driver.get(FORM_LINK)

# inputs all the data scraped from zillow and inputs into google sheets
for ads, prc, lnk in zip(address, price, complete_link):

    address_input = driver.find_element(By.CSS_SELECTOR, 'input[aria-labelledby="i1"]')
    price_input = driver.find_element(By.CSS_SELECTOR, 'input[aria-labelledby="i5"]')
    link_input = driver.find_element(By.CSS_SELECTOR, 'input[aria-labelledby="i9"]')
    submit = driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div/span/span')

    address_input.send_keys(ads)
    price_input.send_keys(prc)
    link_input.send_keys(lnk)
    time.sleep(2)
    submit.click()
    time.sleep(3)
    submit_another = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    submit_another.click()
    time.sleep(3)




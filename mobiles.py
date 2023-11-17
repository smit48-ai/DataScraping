from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller
from bs4 import BeautifulSoup
import requests
import time
import csv


# Check if the current version of chromedriver exists
# and if it doesn't exist, download it automatically,
# then add chromedriver to path

chromedriver_autoinstaller.install() 
driver = webdriver.Chrome()

# Open the webpage
url="https://www.justdial.com/Ahmedabad/Mobile-Shops"
driver.get(url)


def get_mobiles_shop_data(page_source):
    # response = requests.get(url,headers=agent)
    soup = BeautifulSoup(page_source, 'html.parser')
    shop_details=[]
    print(soup.select('.resultbox_textbox'))
    for item in soup.select('.resultbox_textbox'):
        name=item.select('.resultbox_title')[0].text
        address=item.select('.resultbox_address')[0].text
        shop_details.append({
            'name':name,
            'address':address
        })
    return shop_details

def save_to_csv(temples, filename='mobile_shops_in_ahmedabad.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'address']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for temple in temples:
            writer.writerow(temple)


# agent = {"User-Agent":'Mozilla/5.0 (Windows NT 1003; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}

if __name__ == "__main__":
    # Scroll down to load more content
    scrolls = 10  # Adjust the number of scrolls based on the amount of content you want to load
    for _ in range(scrolls):
        # Scroll down using JavaScript
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight-2600);")
        # Wait for the new content to load (you might need to adjust the wait time)
        time.sleep(2)
        
    page_source = driver.page_source
    print(page_source)
    save_to_csv(get_mobiles_shop_data(page_source))
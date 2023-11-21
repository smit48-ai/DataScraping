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
url1="https://www.justdial.com/Ahmedabad/Local-Business-Listing-Services/nct-12123981"
url2="https://dir.indiamart.com/search.mp?ss=business+listing"



def get_data_from_justdial(page_source):
    # response = requests.get(url,headers=agent)
    soup = BeautifulSoup(page_source, 'html.parser')
    business_details=[]
    print(soup.select('.resultbox_textbox'))
    for item in soup.select('.resultbox_textbox'):
        if(item.select('.resultbox_title')):
            name=item.select('.resultbox_title')[0].text
        else: name=""
        if(item.select('.resultbox_address')):
            address=item.select('.resultbox_address')[0].text
        else: address=""
        if(item.select('.resultbox_totalrate')):
            rating=item.select('.resultbox_totalrate')[0].text
        else: rating=""
        business_details.append({
            'name':name,
            'address':address,
            'rating':rating
        })
    return business_details

def get_data_from_indimart(page_source):
    # response = requests.get(url,headers=agent)
    soup = BeautifulSoup(page_source, 'html.parser')
    business_details=[]
    print(soup.select('.prd-card'))
    for item in soup.select('.prd-card'):
        # print(item.select('.prd-name'))
        if(item.select('.prd-name')):
            name=item.select('.prd-name')[0].text
        else: name=""
        # if(item.select('.tac')):
        #     address=item.select('.tac')[0].text
        # else: address=""
        if(item.select('.prc')):
            price=item.select('.prc')[0].text
        else: price=""
        # address=item.select('.tac')[0].text
        # price=item.select('.prc')[0].text
        business_details.append({
            'name':name,
            # 'address':address,
            'price':price
        })
    return business_details

def save_to_csv1(temples, filename='Business_listing_indimart.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name','price']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for temple in temples:
            writer.writerow(temple)
            
def save_to_csv2(temples, filename='Business_listing_justdial.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'address','rating']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for temple in temples:
            writer.writerow(temple)           


# agent = {"User-Agent":'Mozilla/5.0 (Windows NT 1003; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}

if __name__ == "__main__":
    # Scroll down to load more content
    driver.get(url1)
    scrolls = 10  # Adjust the number of scrolls based on the amount of content you want to load
    for _ in range(scrolls):
        # Scroll down using JavaScript
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight-2600);")
        # Wait for the new content to load (you might need to adjust the wait time)
        time.sleep(2)
        
    page_source = driver.page_source
    save_to_csv2(get_data_from_justdial(page_source))

    driver.get(url2)
    # scrolls = 10  # Adjust the number of scrolls based on the amount of content you want to load
    # for _ in range(scrolls):
    #     # Scroll down using JavaScript
    #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight-2600);")
    #     # Wait for the new content to load (you might need to adjust the wait time)
    #     time.sleep(2)

    page_source = driver.page_source
    save_to_csv1(get_data_from_indimart(page_source))
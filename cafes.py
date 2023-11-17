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
url="https://www.google.com/maps/search/cafe+in+ahmedabad/@23.0250051,72.5219204,12.24z/data=!4m2!2m1!6e5?entry=ttu"
driver.get(url)

def get_cafes_data(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')
    cafes=[]
    for item in soup.select('.NrDZNb'):
        detail=[]
        detail.append(item.text)
        cafes.append(detail)
    return cafes

def is_element_scrollable(driver, element):
    # Check if the element has a vertical scrollbar
    return driver.execute_script(
        'return arguments[0].scrollHeight > arguments[0].clientHeight;', element
    )

# agent = {"User-Agent":'Mozilla/5.0 (Windows NT 1003; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
def save_to_csv(cafes, filename='cafes_in_ahmedabad.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name']
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)
        for cafe in cafes:
            print(cafe)
            writer.writerow(cafe)


if __name__ == "__main__":
    scrollable_element = driver.find_elements(By.CLASS_NAME, 'ecceSd')[1]
    if is_element_scrollable(driver, scrollable_element):
        print('The element is scrollable.')
    else:
        print('The element is not scrollable.')
    scrolls = 20
    for _ in range(scrolls):
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", scrollable_element)
        time.sleep(2)
        
    page_source = driver.page_source
    # print(page_source)
    save_to_csv(get_cafes_data(page_source))
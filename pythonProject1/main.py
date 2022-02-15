import csv
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
from bs4 import BeautifulSoup

driver = webdriver.Chrome()
url = 'https://ycharts.com/indicators/us_pmi'
driver.get(url)
time.sleep(1)

table = driver.find_element(By.CLASS_NAME, 'col-md-8')

print(table.text)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
tags = soup.find_all(class_='col-md-8')
data =[]

for i in tags:
    nalzza = i.find(class_='text-right')
    data.append([nalzza])


print(data)
driver.quit()



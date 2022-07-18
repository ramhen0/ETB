# This one has issue with pdf file
from bs4 import BeautifulSoup
import requests

from selenium import webdriver
import re
from time import sleep
import os
import csv
from selenium.webdriver.chrome.service import Service


each_product_link="https://www.etb-tech.com/brocade-emc-ds-6510b-ra-48-x-16gb-sfp-24-active-switch-w-2-x-psu-nob-sw01572.html"
s=Service('C:\\Users\\Mehra\\Desktop\\Python\\chromedriver_here\\chromedriver.exe')

driver = webdriver.Chrome(service=s)
driver.get(each_product_link)
sleep(2)
html=driver.page_source
soup= BeautifulSoup(html,'lxml')
print("Now we will check if this product has Tech Sheet attached to it or not!")
tech_sheet_link=soup.find('div', class_="data item content productattach")
driver.quit()


name_for_pics_again= "Brocade EMC DS-6510B RA 48 x 16Gb SFP+ (24 Active) Switch w/ 2 x PSU - NOB"


if tech_sheet_link is None:
    print("No Tech Sheet! Moving on to next product!")
else:
    response = requests.get(tech_sheet_link.a["href"])
    name_for_pics_again1=name_for_pics_again.replace("w/","with")
    with open(name_for_pics_again1+".pdf", 'wb') as f:
        f.write(response.content)
        f.close()

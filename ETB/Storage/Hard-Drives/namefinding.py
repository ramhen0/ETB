
from bs4 import BeautifulSoup
import requests
import math
from selenium import webdriver
import re
from time import sleep
import os
import csv
from selenium.webdriver.chrome.service import Service


olink="https://www.etb-tech.com/storage/hard-drives"

s=Service('C:\\Users\\Mehra\\Desktop\\Python\\chromedriver_here\\chromedriver.exe')
regex= re.compile("^item product")

driver = webdriver.Chrome(service=s)
driver.get(olink)
sleep(1)
html=driver.page_source
soup= BeautifulSoup(html,'lxml')
driver.quit()

find_each_link=soup.find("li", {"class": regex})
link=find_each_link.find("a",class_="product-item-link").text.strip()

print(link)


from bs4 import BeautifulSoup
import requests
import math
from selenium import webdriver
import re
from time import sleep
import os
import csv
from selenium.webdriver.chrome.service import Service


olink="https://www.etb-tech.com/dell-equallogic-500gb-sas-7-2k-3-5-hard-drive-m63p8-in-ps4100-ps6100-caddy.html"

s=Service('C:\\Users\\Mehra\\Desktop\\Python\\chromedriver_here\\chromedriver.exe')


driver = webdriver.Chrome(service=s)
driver.get(olink)
sleep(1)
html=driver.page_source
soup= BeautifulSoup(html,'lxml')
driver.quit()
counter_image=0
#images=soup.find("div",id="mtImageContainer")
print(soup.find_all("div",class_="mcs-item"))
if len(soup.find_all("div",class_="mcs-item")) == 0:
    images=soup.find_all("div",id="mtImageContainer")
    print("we are inside")
    for x in images:
        product_image_link=x.a["href"]
        print(product_image_link)
        counter_image=counter_image+1
        driver = webdriver.Chrome(service=s)
        driver.get(product_image_link)
        sleep(1)

        current_directory=os.getcwd()
        driver.get_screenshot_as_file(current_directory+ "\\" +"("+str(counter_image)+")" +".png")
    driver.quit()

else:
    images=soup.find_all("div",class_="mcs-item")
    print(images)
    for x in images:
        product_image_link=x.a["href"]
        print(product_image_link)
        counter_image=counter_image+1
        driver = webdriver.Chrome(service=s)
        driver.get(product_image_link)
        sleep(1)
        current_directory=os.getcwd()
        driver.get_screenshot_as_file(current_directory+ "\\" +"("+str(counter_image)+")" +".png")
    driver.quit()

'''
print("Getting Product Images")

for x in images:
    product_image_link=x.a["href"]
    print(product_image_link)
'''

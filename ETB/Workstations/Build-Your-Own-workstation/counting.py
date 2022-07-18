# This program was created to find how many features did the products have. There were some products with varying degree of features. So we calcluated the number of products with respect to their features. this
# was used to solve the problem in Supermicro

from bs4 import BeautifulSoup
import requests
import math
from selenium import webdriver
import re
from time import sleep
import os
import csv
from selenium.webdriver.chrome.service import Service
from collections import Counter


regex= re.compile("^item product")
s=Service('C:\\Users\\Mehra\\Desktop\\Python\\chromedriver_here\\chromedriver.exe')
olink="https://www.etb-tech.com/servers/build-to-order/build-your-own-workstation"
total=[]
# it will have to go through 6 pages for all the 117 products
for x in range(1, 2):
    driver = webdriver.Chrome(service=s)
    driver.get(olink+"?p="+str(x)+"&product_list_limit=21")

    html=driver.page_source
    soup= BeautifulSoup(html,'lxml')
    driver.quit()
# Looking for classes inside 'li' tag with the regular expression
    find_each_link=soup.find_all("li", {"class": regex})
    print("Finding Lists of products on this page")
#    driver.close()
    # This quit needs to happen at the very end so when being outside the lopp

    #counter1=0
#    driver = webdriver.Chrome('C:\\Users\\Mehra\\Desktop\\Python\\chromedriver_here\\chromedriver.exe')

    for link_to_single_product in find_each_link:
        print("Now I am getting information for each product")
        driver = webdriver.Chrome(service=s)
        each_product_link=link_to_single_product.a['href']
        driver.get(each_product_link)
        sleep(2)
        html=driver.page_source
        soup= BeautifulSoup(html,'lxml')
        print("I have extracted the information, its time to put it in order")

        driver.quit()


        #product_info1=soup.find("span",{'class':'base'})
        product_info1=soup.find("span", class_="base").text

        # Description from the table
        descriptions=soup.find("table", class_="table striped")
        each=descriptions.find_all("td")

        counter_image=0


        for individual in each:
            counter_image=counter_image+1
        print(product_info1)
        print(counter_image)
        total.append(counter_image)
        print(Counter(total).items())
        # Images Links

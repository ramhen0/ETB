from bs4 import BeautifulSoup
import requests
import math
from selenium import webdriver
import re
from time import sleep
import os
import csv
from selenium.webdriver.chrome.service import Service

des_list=[]
final_des_list=[]

olink="https://www.etb-tech.com/dell-poweredge-mx7000-with-mx740c-blades-configure-to-order-btomx7000.html"

s=Service('C:\\Users\\Mehra\\Desktop\\Python\\chromedriver_here\\chromedriver.exe')
driver = webdriver.Chrome(service=s)

driver.get(olink)
html=driver.page_source

soup= BeautifulSoup(html,'lxml')
driver.quit()

descrption=soup.find("div",class_="data item content descriptions")
descr=descrption.text.strip()
print(descr)

print(len(descr))
counter=0
first_val=0
flag=0
for x in range(0,len(descr)):

    if descr[x] == '\n' and flag==0 :
        flag=flag=1
        des_list.append(descr[:x])
        counter=x
    elif descr[x] == '\n':
        des_list.append(descr[counter+1:x])
        counter=x
#    else:
#        print("show time")



print(des_list)
print(len(des_list))

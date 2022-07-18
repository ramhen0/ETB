import csv
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import os
from time import sleep
from selenium.webdriver.chrome.service import Service


olink="https://www.etb-tech.com/dell-poweredge-r630-sata-configure-to-order.html"

s=Service('C:\\Users\\Mehra\\Desktop\\Python\\chromedriver_here\\chromedriver.exe')
driver = webdriver.Chrome(service=s)

driver.get(olink)

html=driver.page_source

soup= BeautifulSoup(html,'lxml')

driver.quit()


product_details=[]

all_products=[]
#product_info1=soup.find("span",{'class':'base'})
product_info1=soup.find("span", class_="base").text
product_info2=soup.find("span", class_="sub-title").text

product_details.append(product_info1)

product_details.append(product_info2)
# Description from the table
descriptions=soup.find("table", class_="table striped")
each=descriptions.find_all("td")

counter_image=0
for x in range(1,24,2):
    each_thing=each[x].text.strip()
    product_details.append(each_thing)
# Images Links

all_products.append(product_details)

images=soup.find_all("div",class_="mcs-item")
driver = webdriver.Chrome(service=s)
for link in images:
    counter_image=counter_image+1
    product_image_link=link.a["href"]
    driver.get(product_image_link)
    sleep(1)
    product_info1=product_info1.replace('"', "inch")
    current_directory=os.getcwd()
    driver.get_screenshot_as_file(current_directory+ "\\" +product_info1+str(counter_image) +".png")

driver.quit()

# Saving the information into CSV file
header= ["Detail","Sub-Detail", 'CPU', 'RAM', 'Hard Drives' ,"RAID Controller", "Network Card", "Power Supply", "Remote Access", "Rack Rails", "Bezel", "BackPlanes", "Chassis Type", "Additional Information"]

with open('hello.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(header)
    # write multiple rows
    writer.writerows(all_products)

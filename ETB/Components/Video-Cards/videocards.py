from bs4 import BeautifulSoup
import requests
import math
from selenium import webdriver
import re
from time import sleep
import os
import csv
from selenium.webdriver.chrome.service import Service



product_details=[]

all_products=[]

# This was required as my classes contain two different names so I had to find a regular expression that would match with the first part of class name which both those classes shares
regex= re.compile("^item product")

olink="https://www.etb-tech.com/components/controllers-cards/graphic-cards"

s=Service('C:\\Users\\Mehra\\Desktop\\Python\\chromedriver_here\\chromedriver.exe')
driver = webdriver.Chrome(service=s)

driver.get(olink)
sleep(2)
html=driver.page_source

soup= BeautifulSoup(html,'lxml')
driver.quit()


# Locating and finding the total pages for this category
total_pages=soup.find("div", class_="toolbar toolbar-products")
total_products=total_pages.find("p").text.strip()


counter_to_find_space=0
while(total_products[counter_to_find_space] != " "):
    counter_to_find_space=counter_to_find_space+1

total_number=total_products[:counter_to_find_space]

# The rason I need to add 1 is because I am starting my for loop from 1 because of page starting from 1
outer_iterations=math.ceil(int(total_number)/21)+1


for x in range(1, outer_iterations):
    driver = webdriver.Chrome(service=s)
    driver.get(olink+"?p="+str(x)+"&product_list_limit=21&product_list_mode=grid")
    sleep(2)
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
        product_info2=soup.find("span", class_="sub-title").text

        product_details.append(product_info1)

        product_details.append(product_info2)

        product_details.append(each_product_link)
        # Description from the table
        descriptions=soup.find("table", class_="table striped")
        each=descriptions.find_all("td")

        counter_image=0
        print(product_info1)

        for x in range(1,22,2):

            each_thing=each[x].text.strip()
            product_details.append(each_thing)
        # Images Links

        all_products.append(product_details)

        product_details=[]
#redundant
        driver = webdriver.Chrome(service=s)
        driver.get(each_product_link)
        sleep(2)
        html=driver.page_source
        soup= BeautifulSoup(html,'lxml')

        print("One Image")
        image2= soup.find_all("div",id="mtImageContainer")

# The code has gottne up to this point but its not being executed after this. Also images are not being saved
        for x_image2 in image2:
            driver = webdriver.Chrome(service=s)

            product_image_link=x_image2.a["href"]
            if product_image_link != "#":
                counter_image=counter_image+1
                driver.get(product_image_link)
                sleep(2)
                current_directory=os.getcwd()
                driver.get_screenshot_as_file(current_directory+ "\\" +product_info1+product_info2+"("+str(counter_image)+")" +".png")

            driver.quit()


#driver.close()
header= ["Detail","Sub-Detail", "Link Page",'Model', 'Memory Size', 'Memory Type' ,"Memory Bus", "Memory Bandwidth", "Base Clock", "Turbo Clock", "Thermal Solution", "Height", "Length","Bracket","Outputs","Maximum Power Consumption","Power Connectors Required", "Additional Information" ]

file_name=os.path.basename(__file__)[:-3]
# name the file after the file
with open( file_name+'.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(header)
    # write multiple rows
    writer.writerows(all_products)

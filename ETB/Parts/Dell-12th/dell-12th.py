# Some products dont share the same description. They are not in table form like the code is expecting. Just need to write a case where the description is not in the format expected so we can skip it or fill entires with *
# This one has different description features but also doesnt have description table.

from bs4 import BeautifulSoup
import requests
import math
from selenium import webdriver
import re
from time import sleep
import os
import csv
from selenium.webdriver.chrome.service import Service


product_details_twelve=[]
all_products_twelve=[]


product_details_notable=[]
all_products_notable=[]


# This was required as my classes contain two different names so I had to find a regular expression that would match with the first part of class name which both those classes shares
regex= re.compile("^item product")
olink="https://www.etb-tech.com/parts/dell-12th-generation-servers"
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

# if-else statment begins here
        #product_info1=soup.find("span",{'class':'base'})
        product_info1=soup.find("span", class_="base").text
        try:
            soup.find("span", class_="sub-title").text
        except AttributeError:
            product_info2="None"
        else:
            product_info2=soup.find("span", class_="sub-title").text

        # Description from the table
        descriptions=soup.find("table", class_="table striped")
        each=descriptions.find_all("td")

        counter_image=0
        print(product_info1)

        if len(each)==12:

            product_details_twelve.append(product_info1)

            product_details_twelve.append(product_info2)
            product_details_twelve.append(each_product_link)

            for x in range(1,12,2):

                each_thing=each[x].text.strip()
                product_details_twelve.append(each_thing)
            all_products_twelve.append(product_details_twelve)
            product_details_twelve=[]

        else:
    # This is the case for the no table that gives me 16 features from wrong table

            product_details_notable.append(product_info1)

            product_details_notable.append(product_info2)

            product_details_notable.append(each_product_link)

            driver = webdriver.Chrome(service=s)
            driver.get(each_product_link)
            sleep(2)
            html=driver.page_source

            soup= BeautifulSoup(html,'lxml')
            driver.quit()

            descrption=soup.find("div",class_="data item content descriptions")
            descr=descrption.text.strip()
            counter_notable=0
            first_val=0
            flag=0
            for x in range(0,len(descr)):

                if descr[x] == '\n' and flag==0 :
                    flag=flag=1
                    product_details_notable.append(descr[:x])
                    counter_notable=x
                elif descr[x] == '\n':
                    product_details_notable.append(descr[counter_notable+1:x])
                    counter_notable=x
            #    else:
            #        print("show time")

            all_products_notable.append(product_details_notable)
            product_details_notable=[]

#redundant
        driver = webdriver.Chrome(service=s)
        driver.get(each_product_link)
        sleep(2)
        # This is the source of the WebdriverException error. This needed to be delayed by another second
        html=driver.page_source
        soup= BeautifulSoup(html,'lxml')
        driver.quit()

        print("Launching new window for images screenshot")

        image1= soup.find_all("div",class_="mcs-item")
        counter_image=0

        if len(image1)==0:

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

        else:
# it opened the second product images but didnt take the screenshot
            print("Multiple images")


            for x_image1 in image1:
                driver = webdriver.Chrome(service=s)

                product_image_link=x_image1.a["href"]
                if product_image_link != "#":
                    counter_image=counter_image+1
                    driver.get(product_image_link)
                    sleep(2)
                    current_directory=os.getcwd()
                    driver.get_screenshot_as_file(current_directory+ "\\" +product_info1+product_info2+"("+str(counter_image)+")" +".png")
                driver.quit()


file_name=os.path.basename(__file__)[:-3]




header_twelve= ["Detail","Sub-Detail","Link Page", 'Model', 'IDRAC', 'Server Compatibility' ,"Heat Sinks", "Alternative Parts Numbers", "Additional Information"]
with open( file_name+"twelve"+'.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(header_twelve)
    # write multiple rows
    writer.writerows(all_products_twelve)

with open( file_name+"notable"+'.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerows(all_products_notable)

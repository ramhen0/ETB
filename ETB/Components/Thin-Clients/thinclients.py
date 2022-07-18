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


product_details_twentyeight=[]
all_products_twentyeight=[]


product_details_notable=[]
all_products_notable=[]

# This was required as my classes contain two different names so I had to find a regular expression that would match with the first part of class name which both those classes shares
regex= re.compile("^item product")

olink="https://www.etb-tech.com/components/miscellaneous/thin-clients"

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
    driver.get(olink+"?p="+str(x)+"&product_list_limit=21")
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

# Here I need to decide how i want the code to proceed

# another try except block goes here if they have table or not
# if else statments
        if len(each)==28:

            product_details_twentyeight.append(product_info1)

            product_details_twentyeight.append(product_info2)

            product_details_twentyeight.append(each_product_link)

            for x in range(1,28,2):

                each_thing=each[x].text.strip()
                product_details_twentyeight.append(each_thing)

            all_products_twentyeight.append(product_details_twentyeight)
            product_details_twentyeight=[]

        else :
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
        # Images Links
#redundant
        driver = webdriver.Chrome(service=s)
        driver.get(each_product_link)
        sleep(2)
        html=driver.page_source
        soup= BeautifulSoup(html,'lxml')
        driver.quit()

        print("Now we will open new window for images screenshot")

        images=soup.find_all("div",class_="mcs-item")

#        driver = webdriver.Chrome('C:\\Users\\Mehra\\Desktop\\Python\\chromedriver_here\\chromedriver.exe')
        for link in images:
            driver = webdriver.Chrome(service=s)

            print("Getting Product Images")
            counter_image=counter_image+1
            product_image_link=link.a["href"]
            driver.get(product_image_link)
            sleep(1)
            product_info1=product_info1.replace('"', "inch")
            current_directory=os.getcwd()
            driver.get_screenshot_as_file(current_directory+ "\\" +product_info1+product_info2+"("+str(counter_image)+")" +".png")
        driver.quit()
#Tech Sheet can go here
#driver.close()


file_name=os.path.basename(__file__)[:-3]

# Header for 24
header_twentyeight= ["Detail","Sub-Detail","Link Page", 'CPU', 'RAM', 'Hard Drives' ,"RAID Controller", "Network Card", "Power Supply", "Remote Access", "Rack Rails", "Bezel", "Backplane", "Chassis Type" ,"Additional Information"]
# name the file after the file
with open( file_name+"twentyeight"+'.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(header_twentyeight)
    # write multiple rows
    writer.writerows(all_products_twentyeight)

with open( file_name+"notable"+'.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerows(all_products_notable)

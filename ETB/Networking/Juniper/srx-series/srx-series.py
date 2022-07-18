
# This one has issue with pdf file
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

#thirty two
product_details_notable=[]
all_products_notable=[]
counter_pdf=0

# This was required as my classes contain two different names so I had to find a regular expression that would match with the first part of class name which both those classes shares
regex= re.compile("^item product")

# Pattern strictly starts with dell
pattern='\AJuniper Networks'


olink="https://www.etb-tech.com/networking/juniper-switches/juniper-srx-series"

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
        name_for_pics=link_to_single_product.find("a",class_="product-item-link").text.strip()
        counter_pdf=counter_pdf+1

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
        counter_image=0
        print(product_info1)

# Here I need to decide how i want the code to proceed

# another try except block goes here if they have table or not
# if else statments
        result=re.search(pattern,product_info1)
        if result:
            product_details.append(product_info1)

            product_details.append(product_info2)

            product_details.append(each_product_link)

            descriptions=soup.find("table", class_="table striped")
            each=descriptions.find_all("td")


            for x in range(1,28,2):

                each_thing=each[x].text.strip()
                product_details.append(each_thing)

            all_products.append(product_details)
            product_details=[]

        else :
# This is the case for the no table that gives me 16 features from wrong table

            product_details_notable.append(product_info1)

            product_details_notable.append(product_info2)

            product_details_notable.append(each_product_link)

            driver = webdriver.Chrome(service=s)
            driver.get(each_product_link)
            sleep(1)
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
                    flag=1
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
        # This is the source of the WebdriverException error. This needed to be delayed by another second
        html=driver.page_source
        soup= BeautifulSoup(html,'lxml')
        driver.quit()

        print("Launching new window for images screenshot")

        image1= soup.find_all("div",class_="mcs-item")
        counter_image=0

        if len(image1)==0:
# This is for complellent with one image
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
                    name_for_pics_again=name_for_pics.replace('w/', "with")

                    current_directory=os.getcwd()
                    driver.get_screenshot_as_file(current_directory+ "\\" +name_for_pics_again+"("+str(counter_image)+")" +".png")

                driver.quit()

        else:
# it opened the second product images but didnt take the screenshot
            print("Two images")
            for x_image1 in image1:
                driver = webdriver.Chrome(service=s)

                product_image_link=x_image1.a["href"]
                if product_image_link != "#":
                    counter_image=counter_image+1
                    driver.get(product_image_link)
                    sleep(2)
                    name_for_pics_again=name_for_pics.replace('w/', "with")
                    current_directory=os.getcwd()
                    driver.get_screenshot_as_file(current_directory+ "\\" +name_for_pics_again+"("+str(counter_image)+")" +".png")
                driver.quit()


        driver = webdriver.Chrome(service=s)
        driver.get(each_product_link)
        sleep(2)
        html=driver.page_source
        soup= BeautifulSoup(html,'lxml')
        print("Now we will check if this product has Tech Sheet attached to it or not!")
        tech_sheet_link=soup.find('div', class_="data item content productattach")
        driver.quit()


        if tech_sheet_link is None:
            print("No Tech Sheet! Moving on to next product!")
        else:
            response = requests.get(tech_sheet_link.a["href"])
            name_for_pics_again1=name_for_pics_again.replace("w/","with")
            with open(name_for_pics_again1+str(counter_pdf)+".pdf", 'wb') as f:
                f.write(response.content)
                f.close()
#driver.close()


file_name=os.path.basename(__file__)[:-3]

# Header for 24
header= ["Detail","Sub-Detail","Link Page", 'Model', 'Ports', 'Active Ports (Licensed)' ,"Power Over Ethernet (PoE)", "Power Supplies Installed", "Air Flow", "Module Expansion Slots", "Operating System", "Licenses Installed","Switching Capacity","Management","Chassis Type","Rack Mounting Kit" ,"Additional Information"]

# name the file after the file
with open( file_name +'.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(header)
    # write multiple rows
    writer.writerows(all_products)

#no header here bruh

with open( file_name+"notable"+'.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerows(all_products_notable)

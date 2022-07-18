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

#thirty two
product_details_twentyeight=[]
all_products_twentyeight=[]

# Eigtheen
product_details_eight=[]
all_products_eight=[]



# This was required as my classes contain two different names so I had to find a regular expression that would match with the first part of class name which both those classes shares
regex= re.compile("^item product")

olink="https://www.etb-tech.com/networking/juniper-switches/juniper-mx-series"

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
        if len(each)==8:


            product_details_eight.append(product_info1)

            product_details_eight.append(product_info2)

            product_details_eight.append(each_product_link)

            for x in range(1,8,2):

                each_thing=each[x].text.strip()
                product_details_eight.append(each_thing)

            all_products_eight.append(product_details_eight)
            product_details_eight=[]

        # Images Links


        # I have two different types of 28. There is a problem now!!!
        # possible solution see if the names have a pattern. It is possible dell precision 7920 rack has standard 28 and then dell power edge mx7000 has different
        # possible regular expression

        else:

            product_details_twentyeight.append(product_info1)

            product_details_twentyeight.append(product_info2)
            product_details_twentyeight.append(each_product_link)

            for x in range(1,28,2):

                each_thing=each[x].text.strip()
                product_details_twentyeight.append(each_thing)
            all_products_twentyeight.append(product_details_twentyeight)
            product_details_twentyeight=[]


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
                    name_for_pics_again=name_for_pics.replace('"', "inch")
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
                    name_for_pics_again=name_for_pics.replace('"', "inch")
                    current_directory=os.getcwd()
                    driver.get_screenshot_as_file(current_directory+ "\\" +name_for_pics_again+"("+str(counter_image)+")" +".png")
                driver.quit()

        driver = webdriver.Chrome(service=s)
        driver.get(each_product_link)
        sleep(1)
        html=driver.page_source
        soup= BeautifulSoup(html,'lxml')
        print("Now we will check if this product has Tech Sheet attached to it or not!")
        tech_sheet_link=soup.find('div', class_="data item content productattach")
        driver.quit()


        if tech_sheet_link is None:
            print("No Tech Sheet! Moving on to next product!")
        else:
            response = requests.get(tech_sheet_link.a["href"])

            with open(product_info1+product_info2+".pdf", 'wb') as f:
                f.write(response.content)
                f.close()
#driver.close()


file_name=os.path.basename(__file__)[:-3]

# Header for 24
header_eight= ["Detail","Sub-Detail","Link Page", "Model","Port","Compatibility" ,"Additional Information"]
# name the file after the file
with open( file_name+"eight"+'.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(header_eight)
    # write multiple rows
    writer.writerows(all_products_eight)

header_twentyeight= ["Detail","Sub-Detail","Link Page", 'Model', 'Ports', 'Active Ports (Licensed)' ,"Power Over Ethernet (PoE)", "Power Supplies Installed", "Air Flow", "Module Expansion Slots", "Operating System", "Licenses Installed","Switching Capacity","Management","Chassis Type","Rack Mounting Kit" ,"Additional Information"]

with open( file_name+"twentyeight"+'.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(header_twentyeight)
    # write multiple rows
    writer.writerows(all_products_details_twentyeight)

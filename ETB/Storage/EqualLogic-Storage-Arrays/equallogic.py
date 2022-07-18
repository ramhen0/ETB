# This category has table description and Tech Sheet -- Yes
# The description varies between 7 and 8 - Done Just need to create table names
# It has two tech sheet - Just have to check if it saves correctly

# Things to change
#If the product_info2 name is configure to order than we need to place into a separate 16 .csv

# Done
from bs4 import BeautifulSoup
import requests
import math
from selenium import webdriver
import re
from time import sleep
import os
import csv
from selenium.webdriver.chrome.service import Service


# twenty eight --> Fourteen
product_details_notable=[]
all_products_notable=[]


# This was required as my classes contain two different names so I had to find a regular expression that would match with the first part of class name which both those classes shares
regex= re.compile("^item product")
counter1=0
olink="https://www.etb-tech.com/storage/equallogic-storage"

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


        # Description from the table
        product_info1=soup.find("span", class_="base").text
        try:
            soup.find("span", class_="sub-title").text
        except AttributeError:
            product_info2="None"
        else:
            product_info2=soup.find("span", class_="sub-title").text


        product_details_notable.append(product_info1)

        product_details_notable.append(product_info2)

# Here we will append the page link into csv file
        product_details_notable.append(each_product_link)

        driver = webdriver.Chrome(service=s)
        driver.get(each_product_link)
        sleep(2)
        html=driver.page_source

        soup= BeautifulSoup(html,'lxml')
        driver.quit()

        descrption=soup.find("div",class_="data item content descriptions")

        if len(descrption)!= 0:

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
        else:
            product_details_notable.append("None")
        #    else:
        #        print("show time")

        all_products_notable.append(product_details_notable)
        product_details_notable=[]


#redundant
        driver = webdriver.Chrome(service=s)
        driver.get(each_product_link)
        sleep(2)
        html=driver.page_source
        soup= BeautifulSoup(html,'lxml')

        print("Now we will open new window for images screenshot")

        images=soup.find_all("div",class_="mcs-item")
        driver.quit()
#        driver = webdriver.Chrome('C:\\Users\\Mehra\\Desktop\\Python\\chromedriver_here\\chromedriver.exe')
        counter_image=0
        for link in images:
            driver = webdriver.Chrome(service=s)

            print("Getting Product Images")
            counter_image=counter_image+1
            product_image_link=link.a["href"]
            if product_image_link != "#":
                print(product_image_link)
                print(product_info1)
                driver.get(product_image_link)
                sleep(1)
                product_info1=product_info1.replace('"', "inch")
                current_directory=os.getcwd()
                driver.get_screenshot_as_file(current_directory+ "\\" +product_info1+"("+str(counter_image)+")" +".png")


        driver.quit()

        driver = webdriver.Chrome(service=s)
        driver.get(each_product_link)

        sleep(2)

        html=driver.page_source
        soup= BeautifulSoup(html,'lxml')
        print("Now we will check if this product has Tech Sheet attached to it or not!")
        tech_sheet_link=soup.find('div', class_="data item content productattach")

        #We have to fix the problem for the .pdf links

        try:
            tech_sheet_link.find_all('p')
        except AttributeError:
            print("No Tech Sheet! Moving on to next product!")
        else:
            multi_links_pdf=tech_sheet_link.find_all('p')
            counter_pdf=0
            for link in multi_links_pdf:
                counter_pdf=counter_pdf+1
                #print(link.a["href"])
#                print(link.use["href"])
                response = requests.get(link.a["href"])
                with open(product_info1+product_info2+'('+str(counter_pdf)+')'+".pdf", 'wb') as f:
                    f.write(response.content)
                    f.close() #didnt solve the probelm

#driver.close()

# I have to create a different Description becasue they are not consistent under this category

# We cannot have a dixed header because different individual products have different number of features
# Fix the header type names
file_name=os.path.basename(__file__)[:-3]

with open( file_name+"notable"+'.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerows(all_products_notable)

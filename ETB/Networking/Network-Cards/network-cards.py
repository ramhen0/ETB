
from bs4 import BeautifulSoup
import requests
import math
from selenium import webdriver
import re
from time import sleep
import os
import csv
from selenium.webdriver.chrome.service import Service


product_details_notable=[]
all_products_notable=[]

# This was required as my classes contain two different names so I had to find a regular expression that would match with the first part of class name which both those classes shares
regex= re.compile("^item product")

olink="https://www.etb-tech.com/networking/network-cards"

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

outer_iterations=2

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
# getting the names from the list view page so we can use this for naming pictures

        name_for_pics=link_to_single_product.find("a",class_="product-item-link").text.strip()

        print("Now I am getting information for each product")
        driver = webdriver.Chrome(service=s)
        each_product_link=link_to_single_product.a['href']
        driver.get(each_product_link)
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


        print(product_info1)

# Here I need to decide how i want the code to proceed

# another try except block goes here if they have table or not
# if else statments

# This is the case for the no table that gives me 16 features from wrong table

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

        # The second condition is never getting executed. The products with table share the same class names and div. It will print random stuff from their table but it will be a clue so we know that product is different
        if len(descrption)!= 0:

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
        else:
            product_details_notable.append("None")
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

                counter_image=counter_image+1
                driver.get(product_image_link)
                sleep(2)
                name_for_pics_again=name_for_pics.replace('/', "over")
                current_directory=os.getcwd()
                driver.get_screenshot_as_file(current_directory+ "\\" +name_for_pics_again+"("+str(counter_image)+")" +".png")
                driver.quit()


        else:
# it opened the second product images but didnt take the screenshot
            print("Multiple images")
            for x_image1 in image1:
                driver = webdriver.Chrome(service=s)

                product_image_link=x_image1.a["href"]

                counter_image=counter_image+1
                driver.get(product_image_link)
                sleep(2)
                name_for_pics_again=name_for_pics.replace('/', "over")
                current_directory=os.getcwd()
                driver.get_screenshot_as_file(current_directory+ "\\" +name_for_pics_again+"("+str(counter_image)+")" +".png")
                driver.quit()



#        driver = webdriver.Chrome('C:\\Users\\Mehra\\Desktop\\Python\\chromedriver_here\\chromedriver.exe')


file_name=os.path.basename(__file__)[:-3]

with open( file_name+"notable"+'.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerows(all_products_notable)


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
product_details_twelve=[]
all_products_twelve=[]

#thirty --> sixteen
product_details_sixteen=[]
all_products_sixteen=[]

# Eigtheen --> sixteenOther
product_details_fourteen=[]
all_products_fourteen=[]

# This was required as my classes contain two different names so I had to find a regular expression that would match with the first part of class name which both those classes shares
regex= re.compile("^item product")
counter1=0
olink="https://www.etb-tech.com/storage/build-your-storage-array"

s=Service('C:\\Users\\Mehra\\Desktop\\Python\\chromedriver_here\\chromedriver.exe')
driver = webdriver.Chrome(service=s)

driver.get(olink)
sleep(1)
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
        descriptions=soup.find("table", class_="table striped")
        each=descriptions.find_all("td")

        counter_image=0


        product_info1=soup.find("span", class_="base").text
        try:
            soup.find("span", class_="sub-title").text
        except AttributeError:
            product_info2="None"
        else:
            product_info2=soup.find("span", class_="sub-title").text

# There is a possibility of adding more if-else clauses to cover all different possibilities of descriptions
        if len(each)==16:
            product_details_sixteen.append(product_info1)

            product_details_sixteen.append(product_info2)

            product_details_sixteen.append(each_product_link)

            for x in range(1,16,2):

                each_thing=each[x].text.strip()
                product_details_sixteen.append(each_thing)

            all_products_sixteen.append(product_details_sixteen)
            product_details_sixteen=[]



        elif len(each)==14 :

            product_details_fourteen.append(product_info1)

            product_details_fourteen.append(product_info2)

            product_details_fourteen.append(each_product_link)

            for x in range(1,14,2):

                each_thing=each[x].text.strip()
                product_details_fourteen.append(each_thing)

            all_products_fourteen.append(product_details_fourteen)
            product_details_fourteen=[]

        # Images Links
        else:

            product_details_twelve.append(product_info1)

            product_details_twelve.append(product_info2)

            product_details_twelve.append(each_product_link)

            for x in range(1,12,2):

                each_thing=each[x].text.strip()
                product_details_twelve.append(each_thing)

            all_products_twelve.append(product_details_twelve)
            product_details_twelve=[]

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
        for link in images:
            driver = webdriver.Chrome(service=s)

            print("Getting Product Images")
            counter_image=counter_image+1
            product_image_link=link.a["href"]
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

# Header for 28
header_twelve= ["Detail","Sub-Detail","Link Page",'Hard Drives' ,"Backplane", "Controllers", "Power Supplies", "Rail Kit" ,"Additional Information"]
# name the file after the file
with open( file_name+"twelve"+'.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(header_twelve)
    # write multiple rows
    writer.writerows(all_products_twelve)
    f.close()

header_fourteen= ["Detail","Sub-Detail","Link Page","Hard Drives", 'Backplane', 'Controllers', "Power Supplies", "External RAID Controllers", "Rail Kit","Additional Information"]
with open( file_name+"fourteen"+'.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(header_fourteen)
    # write multiple rows
    writer.writerows(all_products_fourteen)
    f.close()

header_sixteen= ["Detail","Sub-Detail","Link Page","Hard Drives", 'Backplane', 'Controllers', "Power Supplies",'External RAID Controllers', "External SAS Controllers", "Rail Kit","Additional Information"]
with open( file_name+"sixteen"+'.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(header_sxiteen)
    # write multiple rows
    writer.writerows(all_products_sixteen)
    f.close()

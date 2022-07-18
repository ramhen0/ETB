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

#twentyeight

product_details_twentyeight_Super=[]
product_details_twentyeight_dellpow=[]
product_details_twentyeight_dellpre=[]

all_products_details_twentyeight_Super=[]
all_products_details_twentyeight_dellpow=[]
all_products_details_twentyeight_dellpre=[]


#thirty
product_details_thirty=[]
all_products_thirty=[]

#thirty two
product_details_thirtytwo=[]
all_products_thirtytwo=[]

# Eigtheen
product_details_twentyfour=[]
all_products_twentyfour=[]


product_details_notable=[]
all_products_notable=[]

# This was required as my classes contain two different names so I had to find a regular expression that would match with the first part of class name which both those classes shares
regex= re.compile("^item product")

olink="https://www.etb-tech.com/servers/build-to-order"

s=Service('C:\\Users\\Mehra\\Desktop\\Python\\chromedriver_here\\chromedriver.exe')
driver = webdriver.Chrome(service=s)

driver.get(olink)
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

        # Description from the table
        descriptions=soup.find("table", class_="table striped")
        each=descriptions.find_all("td")

        counter_image=0
        print(product_info1)

# Here I need to decide how i want the code to proceed

# another try except block goes here if they have table or not
# if else statments
        if len(each)==24:


            product_details_twentyfour.append(product_info1)

            product_details_twentyfour.append(product_info2)

            product_details_twentyfour.append(each_product_link)

            for x in range(1,24,2):

                each_thing=each[x].text.strip()
                product_details_twentyfour.append(each_thing)

            all_products_twentyfour.append(product_details_twentyfour)
            product_details_twentyfour=[]

        # Images Links


        # I have two different types of 28. There is a problem now!!!
        # possible solution see if the names have a pattern. It is possible dell precision 7920 rack has standard 28 and then dell power edge mx7000 has different
        # possible regular expression
        elif len(each)==28:
# That is where i will insert the code and conditions for three different type of 28s
            if "Supermicro" in product_info1:
# change variable name based on the name
                product_details_twentyeight_Super.append(product_info1)

                product_details_twentyeight_Super.append(product_info2)

                product_details_twentyeight_Super.append(each_product_link)

                for x in range(1,28,2):

                    each_thing=each[x].text.strip()
                    product_details_twentyeight_Super.append(each_thing)
                all_products_details_twentyeight_Super.append(product_details_twentyeight_Super)
                product_details_twentyeight_Super=[]

            elif "Dell Precision" in product_info1 :

# change variable name based on the name
                product_details_twentyeight_dellpre.append(product_info1)

                product_details_twentyeight_dellpre.append(product_info2)
                product_details_twentyeight_dellpre.append(each_product_link)
                for x in range(1,28,2):

                    each_thing=each[x].text.strip()
                    product_details_twentyeight_dellpre.append(each_thing)
                all_products_details_twentyeight_dellpre.append(product_details_twentyeight_dellpre)
                product_details_twentyeight_dellpre=[]
# "Dell Poweredge" in product_info1
            else :

# change variable name based on the name

                product_details_twentyeight_dellpow.append(product_info1)

                product_details_twentyeight_dellpow.append(product_info2)
                product_details_twentyeight_dellpow.append(each_product_link)

                for x in range(1,28,2):

                    each_thing=each[x].text.strip()
                    product_details_twentyeight_dellpow.append(each_thing)
                all_products_details_twentyeight_dellpow.append(product_details_twentyeight_dellpow)
                product_details_twentyeight_dellpow=[]


        elif len(each)==30:

            product_details_thirty.append(product_info1)

            product_details_thirty.append(product_info2)
            product_details_thirty.append(each_product_link)

            for x in range(1,30,2):

                each_thing=each[x].text.strip()
                product_details_thirty.append(each_thing)
            all_products_thirty.append(product_details_thirty)
            product_details_thirty=[]
        elif len(each)==32:

            product_details_thirtytwo.append(product_info1)

            product_details_thirtytwo.append(product_info2)
            product_details_thirtytwo.append(each_product_link)

            for x in range(1,32,2):

                each_thing=each[x].text.strip()
                product_details_thirtytwo.append(each_thing)
            all_products_thirtytwo.append(product_details_thirtytwo)
            product_details_thirtytwo=[]

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
        sleep(1)
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
header_twentyfour= ["Detail","Sub-Detail","Link Page", 'CPU', 'RAM', 'Hard Drives' ,"RAID Controller", "Network Card", "Power Supply", "Remote Access", "Rack Rails", "Bezel", "Backplane", "Chassis Type" ,"Additional Information"]
# name the file after the file
with open( file_name+"twentyfour"+'.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(header_twentyfour)
    # write multiple rows
    writer.writerows(all_products_twentyfour)

header_twentyeight_Super= ["Detail","Sub-Detail","Link Page" 'CPU', 'RAM', 'Hard Drives' ,"RAID Controller", "Network Card", "Power Supply", "Remote Access", "Rack Rails", "Bezel", "Backplane", "Chassis Type","Chassis Model","Motherboard" ,"Additional Information"]
with open( file_name+"twentyeight_Super"+'.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(header_twentyeight_Super)
    # write multiple rows
    writer.writerows(all_products_details_twentyeight_Super)

header_twentyeight_dellpow= ["Detail","Sub-Detail","Link Page", 'Chassis',"Chassis Type", 'Chassis Backplane', 'Hard Drives' ,"Power Supply", "Rack Rails",'Blades', "CPU", "RAM", "Hard Drives", "RAID Controller", "Network Card", "Remote Access" ,"Additional Information"]
with open( file_name+"twentyeight_dellpro"+'.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(header_twentyeight_dellpow)
    # write multiple rows
    writer.writerows(all_products_details_twentyeight_dellpow)

header_twentyeight_dellpre= ["Detail","Sub-Detail","Link Page", 'CPU',"Graphics Card", 'RAM', 'Hard Drives' ,"RAID Controller", "Network Card",'Risers', "Power Supply", "Remote Access", "Rack Rails", "Bezel", "Backplane", "Chassis Type" ,"Additional Information"]
with open( file_name+"twentyeight_dellpre"+'.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(header_twentyeight_dellpre)
    # write multiple rows
    writer.writerows(all_products_details_twentyeight_dellpre)

header_thirty= ["Detail","Sub-Detail","Link Page", 'Chassis', 'Chassis Model', 'Chassis Type',"Bezel" , "Rack Rails" ,"Power Supply", "CPU", "RAM","RAID Controller", "Hard Drives","Network Card","Remote Access","Backplane","Motherboard", "Additional Information"]
with open( file_name+"thirty"+'.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(header_thirty)
    # write multiple rows
    writer.writerows(all_products_thirty)

header_thirtytwo= ["Detail","Sub-Detail","Link Page", 'Chassis', 'Chassis Model', 'Chassis Type' ,"Power Supply", "Rack Rails", "Bezel", "Nodes", "CPU", "RAM", "Hard Drives", "Backplane","RAID Controller","Network Card","Remote Access","Motherboard Model", "Additional Information"]
with open( file_name+"thirtytwo"+'.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(header_thirtytwo)
    # write multiple rows
    writer.writerows(all_products_thirtytwo)

#no header here bruh

with open( file_name+"notable"+'.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerows(all_products_notable)

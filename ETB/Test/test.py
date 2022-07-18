
# This is the most complete code as of 6/19/2022
from bs4 import BeautifulSoup
import requests
import math
import csv
from selenium import webdriver
from time import sleep
import os


# This is where the link goes
olink="https://www.itechdevices.ae/apc.html"

# Everything that follows is shared with

url=requests.get(olink+"?p=1").text

soup = BeautifulSoup(url,'lxml')

# This is my list of lists
all_products=[]

# This is my each product list which would be inside list of lists
each_product=[]

# Extract total iteration number to set the outer for loop

# We will use if loop so that if they have only one page we ca sign outer_iterations=2
total = soup.find("div", class_="count-container")
if total is None:
    outer_iterations=2

else:
    number=total.find("p").text.strip()
    length_char=len(number)
    temp=length_char-1

# While loops to go over so we can find how many digits
    while(number[temp] != ' '):
        temp=temp-1

# This is so we can find the number of digits
    pages=(length_char-1)-temp

# We will extract the total page number and we know
    total_number=number[-pages:]

# Converting the string to integer
    outer_iterations=math.ceil(int(total_number)/12)+1


for x in range(1, outer_iterations):

# main url
    url=requests.get(olink+"?p="+str(x)).text
    soup = BeautifulSoup(url,'lxml')
    links=soup.find_all('li',class_="item")

# for loop to go between the 12 products on each page
    for link in links:
        print("New Product being Processed.\n")
        product_link=link.a["href"]
        inside_url=requests.get(product_link).text
        soup = BeautifulSoup(inside_url,'lxml')

# This is so we can get the name
        product_info=soup.find("div",class_="product-primary-column product-shop grid12-5")
        product_name=product_info.h1.text

# Now we have the name, we need to get SKU, detail and availability. Had to use soup again because they could not be found product_info
        product_detail=soup.find_all("td", class_="td-sp")

# Append the name here to each product
        each_product.append(product_name)
        for x in range(0,3):
            product1=product_detail[x].text
# This is for getting the tags, since we know the details are grabbed when x==1 so it will split them when there is space.
            if x==1:
                detail_tags=product1.split(" ")

            each_product.append(product1)

        each_product.append(detail_tags)

        try:
            product_detail[1].a["href"]
        except TypeError:
            additonal_code=soup.find("table", class_='data-table')
            additonal_code_string=str(additonal_code)

# This is important step, solved the problem with the excel file
            each_product.append(additonal_code_string)

            all_products.append(each_product)

# We will add the additonal information from the table by finding it and then appending into the all_products



# This solved my problem for getting individual list
            each_product=[]

# Here I will insert the code to extract the image

            image_info= soup.find("div", class_="product-img-column grid12-4")
            #for link in links:
            ##    print(slink)
            product_image_link=image_info.a["href"]

            driver=webdriver.Chrome(chrome_link)
            driver.get(product_image_link)
            sleep(1)
            product_name=product_name.replace('"', "inch")
            current_directory=os.getcwd()+"\\"+ zeus_file[:-10]
            driver.get_screenshot_as_file(current_directory+ "\\" +product_name+ ".png")
            #driver.get_screenshot_as_file(product_name+".png")
            driver.quit()
            print("")
        else:
# Here we are going to install the .pdf page
            current_directory=os.getcwd()+"\\"+ zeus_file[:-10]
            pdf_link=landing_page+product_detail[1].a["href"]
            response = requests.get(pdf_link)

            with open(current_directory+"//"+product_name+".pdf", 'wb') as f:
                f.write(response.content)

# We will add the additonal information from the table by finding it and then appending into the all_products
            additonal_code=soup.find("table", class_='data-table')
            additonal_code_string=str(additonal_code)

# This is important step, solved the problem with the excel file
            each_product.append(additonal_code_string)

            all_products.append(each_product)

# This solved my problem for getting individual list
            each_product=[]

# Here I will insert the code to extract the image

            image_info= soup.find("div", class_="product-img-column grid12-4")
            #for link in links:
            ##    print(slink)
            product_image_link=image_info.a["href"]

            driver=webdriver.Chrome(chrome_link)
            driver.get(product_image_link)
            sleep(1)
            product_name=product_name.replace('"', "inch")
            #current_directory=os.getcwd()+"\\"+ zeus_file[:-10]
            driver.get_screenshot_as_file(current_directory+ "\\" +product_name+ ".png")
            #driver.get_screenshot_as_file(product_name+".png")
            driver.quit()
            print("")



        #******************************************************************************************************

# Header for .csv file
header= ["Name",'SKU', 'Detail', 'Availability', 'Tags' ,"Additional Info"]

# Getting the current file name so that we dont need to manually update inside

#file_name=os.path.basename(__file__)
#file_name=os.getcwd()+"\\Sapphire\\sapphire.py"
# For the above i still need to use the file variable from zeus.py here to replace the \\Sapphire\\*.py

with open(file[:-3]+'.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(header)
    # write multiple rows
    writer.writerows(all_products)

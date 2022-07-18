import pyautogui as pg
import pywhatkit as pk
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

'''
chrome_link=Service('C:\\Users\\Mehra\\Desktop\\Python\\chromedriver_here\\chromedriver.exe')
driver=webdriver.Chrome(service=chrome_link)

driver.get('https://www.google.ca/')
'''

time.sleep(2)
pk.search("anne frank")
time.sleep(2)
pg.click(1839,925,duration=1)
time.sleep(2)
pg.scroll(600)
pg.click(2704,33,duration=1)

print("Done")

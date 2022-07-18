from bs4 import BeautifulSoup
from googlesearch import search
import pywhatkit as kt
from time import sleep


try:
    kt.search("mehran amin")
    #print(pyautogui.position())
    #pyautogui.click(1330,767)


except:
    print("Dont know whats wrong!")
else:
    print("It worked")

'''

query="pakistan windsor ontario"


for j in search(query, num=15,stop=10,pause=2):
    print(j)
'''

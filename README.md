You need to install python on your computer, if you dont have it already.

Go to cmd
type 
py --version                         -------------------------------(1)
>[Python 3.10.4]

If you dont get the version number, most likely it is not installed.

Hold on to that thought, in the meantime we will install pip that will be used to manage python packages.

In order to insatll pip, follow the steps in the link
https://phoenixnap.com/kb/install-pip-windows

After that dowload python from the following link,
https://www.python.org/downloads/

After everything is done, execute command (1) (py --version),
You should get version number, which also means you have python installed.


You would need to install
- BeautifulSoup
- requests
- selenium

Use the following commands,

py -m pip install BeautifulSoup
py -m pip install requests
py -m pip install selenium


After that you need to download chromedriver
Download the chromedriver (check the version of chrome you have)
https://chromedriver.chromium.org/downloads

Unzip the downloaded file and save the link to that chromedriver.exe file.
 
This link needs to be pasted in zeus.py file.

replace chrome_link="link goes here"
Place the absolute link for the chromedriver inside

Finally, go to ur cmd and change the directory so your inside python folder.




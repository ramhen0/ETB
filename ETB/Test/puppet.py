from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import os

# Use sync version of Playwright
with sync_playwright() as p:
    # Launch the browser
    browser = p.chromium.launch()

    # Open a new browser page
    page = browser.new_page()

    # Create a URI for our test file
    page_path = "file:/" + os.getcwd() + "/example.html"

    # Open our test file in the opened page
    page.goto(page_path)
    page_content = page.content()

    # Process extracted content with BeautifulSoup
    soup = BeautifulSoup(page_content,'lxml')
    print(soup.find(id="test").get_text())

    # Close browser
    browser.close()

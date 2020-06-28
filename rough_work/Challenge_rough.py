# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup

import pandas as pd
import datetime as dt

def scrape_challenge():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=False)
    
    # Run challenge scraping functions and store results in dictionary
    challenge = {
        "title": challenge_title(browser),
        "img_url": challenge_image(browser)
    }
    
    browser.quit()

    return challenge

# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path)

# Set up function to scrape for title and image
def challenge_scrape(browser):
    # Visit URL
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('a.product-item h3', wait_time=1)

    for i in range(4):
        # Find and click the full hemisphere thumbnail 
        hemi_image_elem = browser.find_by_css('a.product-item h3')[i].click()

        # Add try/except for error handling
        try:
            # Parse the resulting html with soup
            html = browser.html
            challenge_soup = BeautifulSoup(html, 'html.parser')

            # Find the title
            title = challenge_soup.find('h2', class_='title').get_text()
        
            # Find the relative image url
            img_url = img_soup.select_one('ul li a').get('href')
            
        except AttributeError:
            return None, None

    return title, img_url

def challenge_image (browser):
# Visit URL
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('a.product-item h3', wait_time=1)

    for i in range(4):
        # Find and click the full hemisphere thumbnail 
        hemi_image_elem = browser.find_by_css('a.product-item h3')[i].click()

        # Add try/except for error handling
        try:
            # Parse the resulting html with soup
            html = browser.html
            img_soup = BeautifulSoup(html, 'html.parser')

            # Find the relative image url
            img_url = img_soup.select_one('ul li a').get('href')
        except AttributeError:
            return None
           
    return img_url
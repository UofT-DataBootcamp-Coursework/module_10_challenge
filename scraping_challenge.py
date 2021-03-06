# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup

import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    news_title, news_paragraph = mars_news(browser)
    
    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres" : challenge_scrape(browser),
        "last_modified": dt.datetime.now()
    }
        
    browser.quit()

    return data
    
# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path, headless=True)

def challenge_scrape(browser):
    # Set the executable path and initialize the chrome browser in splinter
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)
    
    # Visit URL
    url = 'https://2u-data-curriculum-team.s3.amazonaws.com/dataviz-online-content/module_10/Astropedia+Search+Results+_+USGS+Astrogeology+Science+Center.htm'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.item a.product-item', wait_time=1)
    
    # Parse the resulting html with soup
    html = browser.html
    challenge_soup = BeautifulSoup(html, 'html.parser')
    
    # Create empty list to store individual hemi links
    hemispheres = []
    
    for i in (0,2,4,6):
        hemi_link = challenge_soup.select('div.item a.product-item')[i].get('href')
            
        hemispheres.append(hemi_link)
    
    # Create empty list to store hemi title and image
    hemi_challenge = []
    
    for i in range(4):
        # Visit hemisphere link
        url = hemispheres[i]
        browser.visit(url)

        # Parse the resulting html with soup
        html = browser.html
        challenge_soup = BeautifulSoup(html, 'html.parser')
        
        # Find the title
        title = challenge_soup.find('h2', class_='title').get_text()
        
        # Find the relative image url
        img_url = challenge_soup.select_one('ul li a').get('href')
        
        # Add title and image to hemi_challenge
        hemisphere = {
            'title' : title,
            'img_url' : img_url
        }
        
        # append the dict to hemi_challenge
        hemi_challenge.append(hemisphere)
        
    return hemi_challenge

def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # set up the HTML parser
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    
    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')

        # Assign the title and summary text to variables
        slide_elem.find("div", class_='content_title')

        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_='content_title').get_text()
    
        # Use the parent element to find the paragraph text
        news_paragraph = slide_elem.find('div', class_="article_teaser_body").get_text()
        
    except AttributeError:
        return None, None
   
    return news_title, news_paragraph

def featured_image(browser):
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
        
    except AttributeError:
        return None
    
    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
        
    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # scrape the entire table using pandas
        df = pd.read_html('http://space-facts.com/mars/')[0]
    
    except BaseException:
        return None
    
    # Assign columns and set index of dataframe
    df.columns=['description','value']
    df.set_index('description', inplace=True)
    
    # convert df back into HTML-ready code
    return df.to_html()

# end the session
browser.quit()

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())
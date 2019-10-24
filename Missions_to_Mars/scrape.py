from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def Mars_scrape():

    # Creating browser object
    browser = init_browser()
    
    # First URL to visit is NASA for news
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    # Pulling headline and leading paragraph using splinter
    headline = browser.find_by_css(".content_title")[0].text
    article = browser.find_by_css(".article_teaser_body")[0].text

    # New browser object
    browser = init_browser()

    # Changed URL to Mars Weather twitter account 
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

    # class is "TweetTextSize"
    # using splinter within a list comprehension to strip the tweet down to its text; 
    # we want the top tweet, so that's index 0
    mars_weather = [tweet.text.strip() for tweet in browser.find_by_css(".TweetTextSize")][0]

    # New browser object
    browser = init_browser()

    # NASA's JPL website
    url = "https://jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    # Updating Beautiful Soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    img_source = soup.find(class_ = "carousel_item")['style']

    # Needed image string is between two single quotation marks, so I'm splitting
    # I need the second of the three pieces
    img_string = img_source.split("'")[1]
    
    # Need to attach the string to the url
    base_url = "https://jpl.nasa.gov"
    featured_image_url = base_url + img_string

    # New browser object
    browser = init_browser()

    # Change to Space Facts URL
    url = "https://space-facts.com/mars/"
    browser.visit(url)

    # Updating Beautiful Soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # Scraping the table
    table = soup.find_all('table')[0]

    # Using pandas to convert the table
    mars_facts = pd.read_html(str(table))

    # New browser object
    browser = init_browser()

    # Move to USGS for photos of Mars' hemispheres
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    
    # Updating Beautiful Soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # I'll need to do a number of things to get image names and links:

    # 1) Set up a loop to find all the hemisphere names, pulling by h3 tag, 
    #    then cleaning up the names and saving them to a list
    # 2) Set up another loop to find all the paths to the pages that have a link to the larger image
    # 3) Set up a third loop to take browser to the new pages and grab the image link

    # Step 1

    # I'll make a list to contain the titles of the photos
    title = []

    # There are four elements to find, so I'll set this up to loop four times
    i = 0

    while i < 4:
        hemisphere = soup.find_all('h3')[i].text.strip()
        # This strips "Enhanced" off the end of the string
        hemisphere = hemisphere[:-9]
        # Append to my list
        title.append(hemisphere)
        i += 1
    
    # Step 2

    # Now I'll need a list to contain the URL paths
    paths = []

    # It turns out that there are duplicates for each path, so the loop needs to run 8 times instead of 4
    # and I'll increment by two so that I only capture one instance of the path

    i = 0

    while i < 8:
        path = soup.find_all('a', class_ = 'itemLink product-item')[i]['href']
        paths.append(path)
        i+=2

    # Step 3-A

    # I need the base URL so that I can add the path for each new browser visit
    base_url = "https://astrogeology.usgs.gov"

    # I'll make a list to contain full URLs
    url_list = []

    # I'll make the full URLs by attaching the contents of my paths list to the end of the base_url
    for path in paths:
        url = base_url + path
        url_list.append(url)
    # Step 3-B

    # I'll make a list to hold the image url I'm going to scrape
    image_url = []

    # I'll cycle through the URLs in my url_list, taking the browser to each and getting the image URL out

    for url in url_list:
        
        browser.visit(url)
        
        # Beautiful soup needs to be updated for the new URL
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
    
        # Pull out the image link 
        img_source = soup.find('img', class_ = "wide-image")['src']
        
        # The image source URL is just a path, so I'll need to make a full url to add to the list
        img_url = base_url + img_source
        
        # Add to list
        image_url.append(img_url)

    # Now use a while loop to put them into a dictionary
    
    # I'll store them in this list temporarily:
    hemisphere_image_urls = []

    # The while loop will allow me to use an index
    i = 0

    while i < 4:
        hemisphere_image_urls.append(
        {'title': title[i], 'image_url': image_url[i]})
        i += 1

    # Close the browser after scraping
    browser.quit()

    # Dictionary to return

    mars_data = {
        "Mars_News_Headline": headline,
        "Mars_News_Article": article,
        "Mars_Weather": mars_weather,
        "Mars_Featured_Image": featured_image_url,
        "Mars_Facts": mars_facts,
        "Mars_Hemisphere": hemisphere_image_urls

    }

    return mars_data

if __name__ == "__main__":
    data = Mars_scrape()
    print(data)
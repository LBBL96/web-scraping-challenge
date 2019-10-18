from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    Browser("chrome", **executable_path, headless=False)
    browser = init_browser()

    data = {"NASA_scrape": Mars_news(browser), "mars_weather_scrape": mars_weather(browser),
     "JPL_scrape": featured_image_url(browser), "Mars_Facts_scrape": mars_facts(browser), 
     "USGS_scrape": url_and_title(browser)}

    return data

def NASA_scrape(browser):
    
    # URL to visit
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    # Loading Beautiful Soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # Pulling headline and leading paragraph
    headline = browser.find_by_css(".content_title")[0].text
    article = browser.find_by_css(".article_teaser_body")[0].text

    # Putting items in a dictionary
    # Mars_news = {
    #     "headline": headline,
    #     "article": article
    # }
    
    # Close the browser after scraping
    # browser.quit()

    # return Mars_news
    Mars_news = [headline, article]

    return Mars_news

def mars_weather_scrape(browser):
    # browser = init_browser()

    # Mars Weather twitter account 
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

    # Loading Beautiful Soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # class is "TweetTextSize"
    # using Splinter within a list comprehension to strip the tweet down to its text; 
    # we want the top tweet, so that's index 0
    mars_weather = [tweet.text.strip() for tweet in browser.find_by_css(".TweetTextSize")][0]

    # Putting into dictionary
    # weather = {
    #     "Mars_Weather": mars_weather
    # }

    # Close the browser after scraping
    # browser.quit()
    
    return mars_weather

def JPL_scrape(browser):
    # browser = init_browser()

    # NASA's JPL website
    url = "https://jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    # Loading Beautiful Soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    img_source = soup.find(class_ = "carousel_item")['style']

    # Needed image string is between two single quotation marks
    # I need the second of the three pieces
    img_string = img_source.split("'")[1]
    
    # Need to attach the string to the url
    base_url = "https://jpl.nasa.gov"
    featured_image_url = base_url + img_string

    # Put image in a dictionary
    # featured_image = {
    #     "featured_image_url": featured_image_url
    # }

    # Close the browser after scraping
    # browser.quit()

    return featured_image_url

def Mars_Facts_scrape(browser):
    # browser = init_browser()

    # Space Facts
    url = "https://space-facts.com/mars/"
    browser.visit(url)

    # Loading Beautiful Soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # Scraping the table
    table = soup.find_all('table')[0]

    # Using pandas to convert the table
    mars_facts = pd.read_html(str(table))

    # Converting to JSON
    mars_table = mars_facts[0].to_json(orient='records')

    # Close the browser after scraping
    # browser.quit()

    return mars_facts

def USGS_scrape(browser):
    # browser = init_browser()

    # USGS photos of Mars' hemispheres
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

    # I'll make a list to contain the elements; 'title' is what the project calls for
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
    
    # Now I need to make dictionaries for each image, with title and image_url as keys

    # I'll store them in this list:
    hemisphere_image_urls = []

    # Now use a while loop to capture them as separate dictionaries (as opposed to zipping into tuples)
    # The while will allow me to use an index
    i = 0

    # while i < 4:
    #     hemisphere_image_urls.append(
    #     {'title': title[i], 'image_url': image_url[i]})
    #     i += 1

    while i < 4:
        hemisphere_image_urls.append(
        title[i], image_url[i])
        i += 1


    # Close the browser after scraping
    browser.quit()

    url_and_title = [image_url, hemisphere_image_urls]

    return url_and_title

        

if __name__ == "__main__":
    data = init_browser()
    print(data)
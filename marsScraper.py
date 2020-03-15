from splinter import Browser
import time
import pandas as pd
import requests
import pymongo
from bs4 import BeautifulSoup as bs


def call_browser():
    executable_path = {
        "executable_path": r"D:\webdriver\chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=True)


def scrape_mars():

    browser = call_browser()
# Mars News
    mars_news_url = "https://mars.nasa.gov/news/"
    browser.visit(mars_news_url)

    # download and create the soup
    mars_news_html = browser.html
    mars_news_soup = bs(mars_news_html, "html.parser")
    mars_news_title = mars_news_soup.find('div', class_='list_text').find(
        'div', class_='content_title').find('a').text
    mars_news_body = mars_news_soup.find(
        'div', class_="article_teaser_body").text
    Mars = {}

    Mars["mars_news_title"] = mars_news_title
    Mars["mars_news_body"] = mars_news_body
    for item in Mars.values():
        print(item)

# JPL Image Site
    jpl_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_image_url)
    time.sleep(2)

    # browser.find_by_id("full_image").click()
    # time.sleep(2)
    # browser.links.find_by_partial_text("more info").click()
    # base_url = 'https://www.jpl.nasa.gov/spaceimages'
    html = browser.html
    soup = bs(html, "html.parser")
    # result = soup.find("figure", class_="lede")
    # final = base_url+result.a.img["src"]
    # final

    featured_image_url = soup.find('article')['style'].replace(
        'background-image: url(', '').replace(');', '')[1:-1]

    nasa_main_url = 'https://www.jpl.nasa.gov'

    final = nasa_main_url + featured_image_url

# Mars Weather
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)

    time.sleep(4)
    weather_content = requests.get(weather_url).text
    soup = bs(weather_content, 'html.parser')
    latest_tweets = soup.find_all('div', class_='js-tweet-text-container')
    tweets_list = []
    for tweets in latest_tweets:
        tweet_text = tweets.find('p').text
        if 'Sol' and 'pressure' in tweet_text:
            tweets_list.append(tweet_text)
            print(f"{tweet_text}")
            break
        else:
            pass
    mars_weather = tweets_list
# Mars Facts
    facts_url = 'http://space-facts.com/mars/'

    # Use Panda's `read_html` to parse the url
    mars_facts = pd.read_html(facts_url)

    # Find the mars facts DataFrame in the list of DataFrames as assign it to `mars_df`
    mars_df = mars_facts[0]

    # Assign the columns `['Description', 'Value']`
    mars_df.columns = ['Description', 'Value']

    # Set the index to the `Description` column without row indexing
    mars_df.set_index('Description', inplace=True)

    # Save html code to folder Assets
    data = mars_df.to_html()

    # data = mars_df.to_dict(orient='records')  # Here's our added param..


# Mars Hemispheres
    # HTML Object
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    time.sleep(4)
    # HTML Object
    html_hemispheres = browser.html

    # Parse HTML with Beautiful Soup
    # HTML Object
    html_hemispheres = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html_hemispheres, 'html.parser')

    # Retreive all items that contain mars hemispheres information
    items = soup.find_all('div', class_='item')

    # Create empty list for hemisphere urls
    hemisphere_image_urls = []

    # Store the main_ul
    hemispheres_main_url = 'https://astrogeology.usgs.gov'

    # Loop through the items previously stored
    for i in items:
        # Store title
        title = i.find('h3').text

        # Store link that leads to full image website
        img_url = i.find('a', class_='itemLink product-item')['href']

        # Visit the link that contains the full image website
        browser.visit(hemispheres_main_url + img_url)

        # HTML Object of individual hemisphere information website
        partial_img_html = browser.html

        # Parse HTML with Beautiful Soup for every individual hemisphere information website
        soup = bs(partial_img_html, 'html.parser')

        # Retrieve full image source
        img_url = hemispheres_main_url + \
            soup.find('img', class_='wide-image')['src']

        # Append the retreived information into a list of dictionaries
        hemisphere_image_urls.append({"title": title, "img_url": img_url})

    # Display hemisphere_image_urls
    hemisphere_image_urls

    # Display hemisphere_image_urls


# store the data in dictionary to pass to mongo db

    mars_output = {
        "news_title": mars_news_title,
        "news_paragraph": mars_news_body,
        "featured_image_url": final,
        "mars_weather": mars_weather,
        "hemi_images": hemisphere_image_urls,
        "data": data
    }
    return mars_output
    # browser.quit()

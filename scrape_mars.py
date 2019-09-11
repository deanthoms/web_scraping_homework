#!/usr/bin/env python
# coding: utf-8

# # Mission to Mars - Web Scraping Homework
# ## Dean Thoms
# ### 09-01-2019


# Import necessary dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd


# # Step 1 - Scraping


def scrape():
    # Use splinter to establish browswer route
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', headless=False)


    # ### Nasa Mars News Scrape


    ## Nasa Mars News
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')


    news_title = soup.find('div', class_= "list_text").find('div', class_="content_title").get_text()
    news_p = soup.find('div', class_= "list_text").find('div', class_="article_teaser_body").get_text()


    # ### JPL Mars Space Images Scrape

    ## JPL Mars Images
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html,'html.parser')


    featured_image_1 = soup.find('a', class_="button fancybox").get('data-fancybox-href')
    featured_image_url = 'https://www.jpl.nasa.gov' + featured_image_1
    

    ### Mars Weather
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html,'html.parser')

    mars_weather = soup.find('div',class_= 'stream-container').find('div', class_='stream').find('li', class_='js-stream-item stream-item stream-item').find('div', class_= 'content').find('div', class_= 'js-tweet-text-container').find('p').get_text()


    # ### Mars Facts


    ## Mars Facts
    url = 'https://space-facts.com/mars/'

    table = pd.read_html(url)
    
    df = table[1]

    df.columns = ['Description:', 'Value:']

    df_html = df.to_html(index = False, justify = 'center', table_id = 'pandas_table', header = ['Desc:', 'Value:'])


    # ### Mars Hemispheres


    ### Mars hemispheres
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html,'html.parser')

    results = soup.find_all('div', class_="description")

    hemisphere_image_urls = []

    # Link to subdomain
    for result in results:
        title = result.find('a', class_='itemLink product-item').find('h3').get_text()
        image_link = 'https://astrogeology.usgs.gov/' + result.find('a', class_='itemLink product-item').get('href')
        browser.visit(image_link)
        html_img = browser.html
        soup_img = BeautifulSoup(html_img,'html.parser')

        image_url = soup_img.find('div',class_='container').find('div', class_='downloads').find('li').find('a').get('href')

        #Insert data into dictionary
        hemisphere_image_urls.append( {
                'title': title,
                'url': image_url
                })

    dict = {
        'news_title': news_title,
        'news_p': news_p,
        'featured_image_url': featured_image_url,
        'mars_weather': mars_weather,
        'df_html': df_html,
        'hemisphere_image_urls': hemisphere_image_urls
        }

    return dict







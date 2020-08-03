#Dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import time

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_info = {}

    #Mars News
    url_1 = 'https://mars.nasa.gov/news/'
    browser.visit(url_1)

    html = browser.html
    soup = bs(html, 'html.parser')

    mars_info["title"] = soup.find('ul', class_='item_list').find('li', class_='slide').find('div', class_='content_title').find('a').get_text()
    mars_info["paragraph"] = soup.find('ul', class_='item_list').find('li', class_='slide').find('div', class_='article_teaser_body').get_text()


    #Mars Featured Image
    url_2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_2)

    browser.find_by_css('div[class="default floating_text_area ms-layer"]').find_by_css('footer').find_by_css('a[class="button fancybox"]').click()
    browser.find_by_css('div[id="fancybox-lock"]').find_by_css('div[class="buttons"]').find_by_css('a[class="button"]').click()
    mars_info["feat_img"] = browser.find_by_css('div[id="page"]').find_by_css('section[class="content_page module"]').find_by_css('figure[class="lede"]').find_by_css('a')['href']


    #Mars Weather
    url_3 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_3)
    time.sleep(5)
    browser.reload()
    time.sleep(5)
    html = browser.html
    time.sleep(5)
    soup = bs(html, 'html.parser')
    time.sleep(5)
    mars_info["weather"] = soup.find('div', class_='css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0').find('span', class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0').get_text()


    #Mars Facts
    url_4 = 'https://space-facts.com/mars/'

    tables = pd.read_html(url_4)

    mars_df = tables[0]
    mars_df.columns = ['Description', 'FACT']
    mars_df.set_index('Description', inplace=True)
    mars_df.index.name=None
    mars_info["mars_table"] = mars_df.to_html()
    

    #Mars Hemispheres
    url_5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_5)

    html = browser.html
    soup = bs(html, 'html.parser')

    hemispheres = soup.find('div', class_='collapsible results').find_all('div', class_='item')

    hemisphere_dict = []
    for x in range(len(hemispheres)):
        title = hemispheres[x].find('div', class_="description").find('h3').text
        browser.find_by_css('div[class="collapsible results"]').find_by_css('div[class="item"]')[x]    .find_by_css('div[class="description"]').find_by_css('a').click()
    
        for img in browser.find_by_css('div[class="downloads"]').find_by_css('a'):
            if ('Original' in img.text):
                img_url = img['href']
        browser.back()
        h_dict = {'caption': title, 'image': img_url}
        hemisphere_dict.append(h_dict)

    mars_info["hemisphere_dict"] = hemisphere_dict

    return mars_info

    browser.quit()



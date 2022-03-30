from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


def scrape_info():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = "https://redplanetscience.com/"
    browser.visit(url)

    time.sleep(5)

    html = browser.html
    soup = bs(html, "html.parser")

    news_title = soup.find('div', class_="content_title").text
    news_p = soup.find('div', class_="article_teaser_body").text

    url = "https://spaceimages-mars.com"
    browser.visit(url)

    full_image_btn = browser.find_by_tag('button')[1]
    full_image_btn.click()

    root_url = "https://spaceimages-mars.com/"
    html = browser.html
    soup = bs(html, "html.parser")
    image = soup.find('img', class_="fancybox-image")
    image_url = image.get('src')
    featured_img_url = root_url + image_url

    df = pd.read_html("https://galaxyfacts-mars.com")[0]
    df.columns=["Description", "Mars", "Earth"]
    df.set_index("Description", inplace=True)
    mars_facts = df.to_html()

    url = "https://marshemispheres.com/"
    browser.visit(url)

    html = browser.html
    soup = bs(html, "html.parser")

    results = soup.find_all('div',class_='item')
    hemisphere_image_urls = []
    for result in results:
        image_dict = {}
        title = result.find("h3").text
        link = result.find("a")["href"]
        image_link = "https://marshemispheres.com/" + link
        browser.visit(image_link)
        time.sleep(3)
        html = browser.html
        soup= bs(html, "html.parser")
        full_size_img = soup.find("img", class_="wide-image")['src']
        full_size_img_link = "https://marshemispheres.com/" + full_size_img
        print(title)
        print(image_link)
        print(full_size_img_link)
        image_dict['title']= title
        image_dict['image_url']= full_size_img_link
        hemisphere_image_urls.append(image_dict)

    nasa_data = {
    "news_title" : news_title,
    "news_p" : news_p,
    "mars_facts": mars_facts,
    "featured_img_url" : featured_img_url,
    "hemisphere_image_urls" : hemisphere_image_urls
    }

    browser.quit()

    return nasa_data
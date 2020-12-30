from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    #NB: Replace path with local path to ChromeDriver
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

#Mars Scrape; The Red Planet Shall be Conquered... also watch the Expanse!
def scrape_info():
    browser = init_browser()
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    soup = bs(html,"html.parser")
    thread = soup.find("div", class_="list_text")
    news_ttl = thread.find("div", class_= "content_title").text
    news_para = thread.find("div", class_="article_teaser_body").text

#image scrape
image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(image_url)
html = browser.html
soup = bs(html,"html.parser")
thread = soup.find("article", class_="carousel_item")
featured_image = thread.find("a", class_="button fancybox")["data-fancybox-href"]                                                       
featured_image_link = "https://www.jpl.nasa.gov/" + featured_image

#hemispheres
hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(hemi_url)     
html = browser.html
soup = bs(html, "html.parser")
results = soup.find_all("div", class_="item")
hemisphere_image_urls = []

 #scrape for mars facts
facts_url = "https://space-facts.com/mars/"
df = pd.read_html(facts_url)
mars_facts = df[0]
mars_facts.columns=["Description", "Mars"]
mars_facts.set_index("Description", inplace=True)
mars_tbl = mars_facts.to_html(classes="table table-bordered")

for result in results:
    title = result.find("h3").text
    hemi_link = result.find("a", class_="itemLink product-item")["href"]
    image_link = "https://astrogeology.usgs.gov/" + hemi_link
    browser.visit(image_link)
    image_html = browser.html
    soup = bs(image_html, "html.parser")
    image_url = "https://astrogeology.usgs.gov/" + soup.find("img", class_="wide-image")["src"]
    hemisphere_image_urls.append({"title":title, "Image_url":image_url})

#create dictionary
mars_dict = {"news_title":news_ttl, "news_text":news_para, "featured_image":featured_image_link , "mars_facts":mars_tbl, "hemi_image_urls":hemisphere_image_urls}

# Close browser session
browser.quit()

#results 
return mars_dict
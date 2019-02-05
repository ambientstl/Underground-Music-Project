
#%%
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import pymongo


#%%
def init_browser():
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


#%%
browser = init_browser()

#set url
url = "https://nodata.tv/blog"
browser.visit(url)

time.sleep(1)

#scrape page into Soup
html = browser.html
soup = bs(html, "html.parser")


#%%
links = []

boxes = soup.find_all("article", class_="project-box")

for box in boxes:
    link = box.find("a", class_="title")["href"]
    links.append(link)

print(links)


#%%
undergroundMusic = []
for link in links:
    browser.visit(link)

    time.sleep(3)

    #scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    
    #find main div
    main = soup.find("div", {"id": "main"})
    
    #find artist, album, year
    title = main.find("h4").text
    artist = title.split("/")[0]
    album = title.split("/ ")[1].split("[")[0]
    year = title.split("[")[1].split("]")[0]
    print(artist, album, year)
    
    #find genre tags in metadata
    metadata = main.find("ul", class_="meta")
    date = metadata.find_all("li")[1].text
    tags = metadata.find_all("li")[2]
    tags = tags.find_all("a")
    #add tags to genres list
    genres = []
    for tag in tags:
        genre = tag.text
        genres.append(genre)
    print(date)
    print(genres)
    
    #find cover img url
    cover_link = main.find("img")["src"]
    print(cover_link)
    
    #find label and catalog number
    label = main.find("section", class_="post").text
    split = label.split("[")
    labeldata = split[1].split("]")[0]
    label = labeldata.split(": ")[1].split(" |")[0]
    catalog = labeldata.split(": ")[2]
    print(label, catalog)

    #compile album info into dict
    albumInfo = {
        "url": link,
        "artist": artist,
        "album": album,
        "year": year,
        "date": date,
        "genres": genres,
        "cover": cover_link,
        "label": label,
        "catalog": catalog
    }
    print(albumInfo)
    
    #add dict to underground music list
    undergroundMusic.append(albumInfo)


#%%
browser.quit()
undergroundMusic


#%%
conn = 'mongodb://localhost:27017/nodata_dev'
client = pymongo.MongoClient(conn)

# Declare the database
db = client["underground_music_db"]

db["nodata_db"].drop()

# Declare the collection
collection = db["nodata_db"]


#%%
undergroundMusic


#%%
collection.insert_many(undergroundMusic)


#%%
results = db.nodata_db.find()
for result in results:
    print(result)



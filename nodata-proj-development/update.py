from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import pymongo

#connect to mongodb
conn = 'mongodb://localhost:27017/underground_music_db'
client = pymongo.MongoClient(conn)
# Declare the database
db = client["underground_music_db"]
# Declare the collection
collection = db["nodata_db"]

#get data
data = collection.find()

#find latest date
dates = []
for album in data:
  dates.append(album["date"])
latestDate = max(dates)
print(f"Latest Blog Date: {latestDate}")

#start browser
def init_browser():
  executable_path = {"executable_path": "chromedriver"}
  return Browser("chrome", **executable_path, headless=False)
browser = init_browser()
#set url
url = "https://nodata.tv/blog"
browser.visit(url)
time.sleep(1)
#scrape page into Soup
html = browser.html
soup = bs(html, "html.parser")

#get 1st page of links
links = []
boxes = soup.find_all("article", class_="project-box")
for box in boxes:
    link = box.find("a", class_="title")["href"]
    links.append(link)

#empty list for new posts
newPosts = []
#visit each link
for link in links:
  browser.visit(link)
  time.sleep(1)
  #scrape page into Soup
  html = browser.html
  soup = bs(html, "html.parser")
  
  #find main div
  main = soup.find("div", {"id": "main"})
  #find date
  metadata = main.find("ul", class_="meta")
  date = metadata.find_all("li")[1].text
  print(f"Latest Database Date: {date}")

  #if date <= latestDate, exit loop
  if date <= latestDate:
    break
  #else, scrape post
  else:
    #find artist, album, year
    title = main.find("h4").text
    artist = title.split("/")[0]
    album = title.split("/ ")[1].split("[")[0]
    year = title.split("[")[1].split("]")[0]
    print(artist, album, year)
    
    #find genre tags in metadata
    # metadata = main.find("ul", class_="meta")
    # date = metadata.find_all("li")[1].text
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
    newPosts.append(albumInfo)

browser.quit()
print(newPosts)

#if there are new posts,
if len(newPosts) > 0:
  #add new posts to db
  collection.insert(newPosts)
else:
  print("Database up to date")

# results = collection.find()
# for result in results:
#   print(result)
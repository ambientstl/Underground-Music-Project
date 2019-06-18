from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, ForeignKey
 
import pymysql
pymysql.install_as_MySQLdb()
from config import mySQLpassword

from splinter import Browser
from bs4 import BeautifulSoup as bs
import time

import datetime as dt

import wikipedia


#initialize browser
def init_browser():
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)
browser = init_browser()


## Scrape Links

#set url
url = "https://nodata.tv/blog"
browser.visit(url)

time.sleep(1)

#scrape first page into Soup
html = browser.html
soup = bs(html, "html.parser")

links = []
#for pages 1 to 50
for i in range(1, 101):
    boxes = soup.find_all("article", class_="project-box")
    
    for box in boxes:
        link = box.find("a", class_="title")["href"]
        links.append(link)
        
    url = "https://nodata.tv/blog/page/" + str(1 + i)
    browser.visit(url)
    time.sleep(1)
    
    #scrape page into soup
    html = browser.html
    soup = bs(html, "html.parser")


## Scrape Album Info

undergroundMusic = []
for link in links:
    browser.visit(link)

    time.sleep(1)

    #scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    
    #find main div
    main = soup.find("div", {"id": "main"})
    
    
    ### ARTIST, ALBUM, YEAR ###
    #find artist, album, year
    title = main.find("h4").text
#     print(title)
    try:
        split_title = title.split(" – ")
        artist = split_title[0]
        album = split_title[1].split(" [")[0]
    except IndexError:
        try:
            split_title = title.split(" / ")
            artist = split_title[0]
            album = split_title[1].split(" [")[0]
        except IndexError:
            split_title = title.split("/")
            artist = split_title[0]
            album = split_title[1].split(" [")[0]
        
    #strip trailing whitespace from artist and album
    artist = artist.strip()
    album = album.strip()
        
    try:
        year = split_title[1].split(" [")[1].split("]")[0]

        try:
            year + 1
        except TypeError:
            #find metadata
            metadata = main.find("ul", class_="meta")
            #find blog post date and isolate year
            date = metadata.find_all("li")[1].text
            year = date.split(", ")[1]

    except IndexError:
        #find metadata
        metadata = main.find("ul", class_="meta")
        #find blog post date and isolate year
        date = metadata.find_all("li")[1].text
        year = date.split(", ")[1]
    
    print("|"+artist+"|"+album+"|"+year+"|")
    
    
    ### DATE, GENRES ###
    #find metadata
    metadata = main.find("ul", class_="meta")
    #find date and convert to datetime object
    date = metadata.find_all("li")[1].text
    date = dt.datetime.strptime(date, "%b %d, %Y")
    #find genre tags in metadata
    tags = metadata.find_all("li")[2]
    tags = tags.find_all("a")
    #add tags to genres list
    genres = []
    for tag in tags:
        genre = tag.text
        genres.append(genre)
        
#     print("|"+date+"|")
#     print("|"+genres+"|")
    
    
    ### ALBUM ART ###
    #find cover img url
    cover_link = main.find("img")["src"]
    #remove 's' from https in link
    cover_link = cover_link.replace("s", "", 1)
#     print(cover_link)
        
    ### LABEL, CATALOG NUMBER ###
    #find label and catalog number
    label_text = main.find("section", class_="post").text
    label_text = label_text.replace("[", "")
    label_text = label_text.replace("]", "")
    label = label_text.split(":")[1].split("|")[0]
    try:
        catalog = label_text.split(":")[2].split("\n")[0]
    except IndexError:
        catalog = label_text.split("Cat#")[1].split("\n")[0]

    #strip whitespace from label and catalog
    label = label.strip()
    catalog = catalog.strip()
    print("|"+label+"|"+catalog+"|")
    
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
    # print(albumInfo)
    
    #add dict to underground music list
    undergroundMusic.append(albumInfo)
    
browser.quit()


## SQL DB Initialization

# Create Engine and Pass in MySQL Connection
engine = create_engine(f"mysql://root:{mySQLpassword}@localhost:3306")

#create and use undergroundMusic db
engine.execute("CREATE DATABASE IF NOT EXISTS undergroundMusic")
engine.execute("USE undergroundMusic")

# Sets an object to utilize the default declarative base in SQL Alchemy
Base = declarative_base()

class Albums(Base):
    __tablename__ = 'Albums'
    id = Column("album_id", Integer, primary_key=True)
    url = Column(String(255))
    artist = Column(String(255))
    album = Column(String(255))
    year = Column(Integer)
    date = Column(Date)
    cover = Column(String(255))
    label = Column(String(255))
    catalog = Column(String(255))
    
class Genres(Base):
    __tablename__ = 'Genres'
    id = Column("genre_id", Integer, primary_key=True)
    name = Column(String(255))
    description = Column(String(8000))

class Album_Genres(Base):
    __tablename__ = 'Album_Genres'
    id = Column("album_genre_id", Integer, primary_key=True)
    album_id = Column(Integer, ForeignKey('Albums.album_id'))
    genre_id = Column(Integer, ForeignKey('Genres.genre_id'))

# Use this to clear out the db
# ----------------------------------
Base.metadata.drop_all(engine)

# ----------------------------------
# Create (if not already in existence) the tables associated with our classes.
Base.metadata.create_all(engine)

## Populate SQL DB
session = Session(bind=engine)

for entry in undergroundMusic:
    album = Albums(url = entry["url"], artist = entry["artist"], album = entry["album"], 
                   year = entry["year"], date = entry["date"], cover = entry["cover"], 
                   label = entry["label"], catalog = entry["catalog"])
    session.add(album)
    
    for item in entry["genres"]:
        exists = session.query(Genres.id).filter_by(name=item).scalar() is not None
        #if item exists in Genres db, skip
        if exists:
            pass
        #else, lookup wiki summary and add item to Genres table
        else:
            try:
                if item == "Album":
                    summary = wikipedia.summary(item)
                elif item == "EP":
                    summary = wikipedia.summary("Extended Play")
                elif item == "Various Artists" or item == "Compilation" or item == "Anthology":
                    summary = wikipedia.summary("Compilation Album")
                elif item == "Leftfield":
                    summary = wikipedia.summary("Progressive House")
                elif item == "Avantgarde":
                    summary = wikipedia.summary("Avant-garde music")
                elif item == "Acid" or item == "Ghetto" or item == "Garage":
                    summary = wikipedia.summary(item + " House")
                elif item == "Beats":
                    summary = wikipedia.summary("Beat (music)")
                elif item == "Boogie":
                    summary = wikipedia.summary("Boogie (genre)")
                elif item == "Remixes":
                    summary = wikipedia.summary("Remix")
                elif item == "Dance Hall":
                    summary = wikipedia.summary("Dancehall")
                elif item == "Live":
                    summary = wikipedia.summary("Concert")
                elif item == "Uncategorized":
                    summary = wikipedia.summary("Experimental Music")
                elif item == "Synth Wave":
                    summary = wikipedia.summary("Synth-pop")
                else:
                    summary = wikipedia.summary(item + " music")
                genre = Genres(name = item, description = summary)
                session.add(genre)
            except wikipedia.exceptions.PageError:
                print(f"Page not found for '{item}' music")
                pass
            time.sleep(3)
            
    session.commit()

for entry in undergroundMusic:
    albumID = session.query(Albums.id).filter_by(url=entry["url"]).scalar()
    
    for genre in entry["genres"]:
        genreID = session.query(Genres.id).filter_by(name=genre).scalar()
        ids = Album_Genres(album_id = albumID, genre_id = genreID)
        session.add(ids)
        session.commit()

print("Database created.")
print(f"{len(undergroundMusic)} albums added.")
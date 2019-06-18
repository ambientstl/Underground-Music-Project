from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine, func

from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

import pymysql
pymysql.install_as_MySQLdb()
from config import mySQLpassword

import pandas as pd
import datetime as dt
import random

app = Flask(__name__)

engine = create_engine(f"mysql://root:{mySQLpassword}@localhost:3306/undergroundMusic")
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://root:{mySQLpassword}@localhost:3306/undergroundMusic"
# engine = create_engine("sqlite:///undergroundMusic.sqlite")
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///undergroundMusic.sqlite"

# reflect the tables
db = SQLAlchemy(app)
Base = automap_base()
Base.prepare(db.engine, reflect=True)

# Assign the classes to a variable 
Albums = Base.classes.albums
Genres = Base.classes.genres
Album_Genres = Base.classes.album_genres

#Necessary? or Flask-SQLAlchemy provides preconfigured 'session'?
# session = scoped_session(sessionmaker(bind=engine))
session = Session(engine)


@app.route("/test")
def test():
  return render_template("test.html")

@app.route("/")
def home():
  results2 = db.session.query(Albums.album_id).all()
  album_ids = [result[0] for result in results2]
  total_albums = len(album_ids)
  return render_template("index.html", total_albums=total_albums)

@app.route("/genre/<genre>")
def genre_analysis(genre):
  results = db.session.query(Genres.name, Genres.description).filter(Genres.name == genre).all()
  name = [result[0] for result in results][0]
  description = [result[1] for result in results][0]

  results3 = db.session.query(Albums.cover).filter(Albums.album_id == Album_Genres.album_id).filter(Album_Genres.genre_id == Genres.genre_id).filter(Genres.name == genre).all()
  covers = [result[0] for result in results3]
  random_covers = random.choices(covers, k=4)

  results4 = db.session.query(Albums.label).filter(Albums.album_id == Album_Genres.album_id).filter(Album_Genres.genre_id == Genres.genre_id).filter(Genres.name == genre).all()
  labels = [result[0] for result in results4]
  label_counts = pd.Series(labels).value_counts()
  label_counts = label_counts.reset_index()
  label_counts = label_counts.rename(columns={"index": "Label", 0: "Count"})
  label_counts = label_counts.to_dict(orient='records')

  results5 = db.session.query(Albums.artist).filter(Albums.album_id == Album_Genres.album_id).filter(Album_Genres.genre_id == Genres.genre_id).filter(Genres.name == genre).all()
  artists = [result[0] for result in results5]
  artist_counts = pd.Series(artists).value_counts()
  artist_counts = artist_counts.reset_index()
  artist_counts = artist_counts.rename(columns={"index": "Artist", 0: "Count"})
  artist_counts = artist_counts.to_dict(orient='records')

  data = {"Name": name, 
  "Description": description, 
  "Covers": random_covers, 
  "Labels": label_counts, 
  "Artists": artist_counts}
  return render_template("genre_analysis.html", Data=data)

@app.route("/genres")
def genre_list():
  return render_template("genre_list.html")

@app.route("/genre_associations")
def genre_associations():
  return render_template("genre_associations.html")

@app.route("/api")
def api():
  data = {
    "Available Routes": ["/api/genres", "/api/top_genres", "/api/genres/<genre>", "/api/genre_associations"]
  }
  return jsonify(data)

@app.route("/api/top_genres")
def top_genres_api():
  #query db for genres
  results = db.session.query(Genres.name).filter(Albums.album_id == Album_Genres.album_id).filter(Genres.genre_id == Album_Genres.genre_id).all()
  #put results into list
  genres = [result[0] for result in results]
  #convert to series and get value counts
  genreCounts = pd.Series(genres).value_counts()
  #reset index and rename columns
  genreCounts = genreCounts.reset_index()
  genreCounts = genreCounts.rename(columns={"index": "Genre", 0: "Count"})

  descriptions = []
  for genre in genreCounts["Genre"]:
    results1 = db.session.query(Genres.description).filter(Genres.name == genre).all()
    description = [result[0] for result in results1][0]
    descriptions.append(description)
  genreCounts["Description"] = descriptions
  #create json of data
  top_genres_data = genreCounts.to_dict(orient='records')

  results2 = db.session.query(Albums.album_id).all()
  album_ids = [result[0] for result in results2]
  total_albums = len(album_ids)

  data = {
    "Total_Albums": total_albums,
    "Top_Genres": top_genres_data
  }

  return jsonify(data)

@app.route("/api/genres")
def genres_api():
  results = db.session.query(Genres.name).all()
  #put results into list
  genres = [result[0] for result in results]
  #get unique entries from list
  genres = list(set(genres))
  genres.sort()
  data = [{"Genres": genres}]
  return jsonify(data)

@app.route("/api/genres/<genre>")
def genre_api(genre):
  results = db.session.query(Genres.name, Genres.description).filter(Genres.name == genre).all()
  name = [result[0] for result in results]
  description = [result[1] for result in results]

  results1 = db.session.query(Album_Genres.album_id).filter(Album_Genres.genre_id == Genres.genre_id).filter(Genres.name == genre).all()
  album_ids = [result[0] for result in results1]
  album_count = [len(results1)]

  results2 = db.session.query(Genres.name).filter(Genres.genre_id == Album_Genres.genre_id).filter(Album_Genres.album_id.in_(album_ids)).all()
  assoc_genres = [result[0] for result in results2]
  assoc_genre_counts = pd.Series(assoc_genres).value_counts()
  assoc_genre_counts = assoc_genre_counts.reset_index()
  assoc_genre_counts = assoc_genre_counts.rename(columns={"index": "Genre", 0: "Associated_Count"})
  assoc_genre_counts = assoc_genre_counts.sort_values(by=["Genre"])

  assoc_genre_totals = []
  for assoc_genre in assoc_genre_counts["Genre"]:
    assoc_results = db.session.query(Album_Genres.album_id).filter(Album_Genres.genre_id == Genres.genre_id).filter(Genres.name == assoc_genre).all()
    assoc_genre_total_count = len(assoc_results)
    assoc_genre_totals.append(assoc_genre_total_count)

  assoc_genre_counts["Total_Count"] = assoc_genre_totals
  assoc_genre_counts = assoc_genre_counts.sort_values(by=["Associated_Count"], ascending=False)
  assoc_genre_counts = assoc_genre_counts.to_dict(orient='records')

  results3 = db.session.query(Albums.cover).filter(Albums.album_id == Album_Genres.album_id).filter(Album_Genres.genre_id == Genres.genre_id).filter(Genres.name == genre).all()
  covers = [result[0] for result in results3]
  random_covers = random.choices(covers, k=4)

  results4 = db.session.query(Albums.label).filter(Albums.album_id == Album_Genres.album_id).filter(Album_Genres.genre_id == Genres.genre_id).filter(Genres.name == genre).all()
  labels = [result[0] for result in results4]
  label_counts = pd.Series(labels).value_counts()
  label_counts = label_counts.reset_index()
  label_counts = label_counts.rename(columns={"index": "Label", 0: "Count"})
  label_counts = label_counts.to_dict(orient='records')

  results5 = db.session.query(Albums.artist).filter(Albums.album_id == Album_Genres.album_id).filter(Album_Genres.genre_id == Genres.genre_id).filter(Genres.name == genre).all()
  artists = [result[0] for result in results5]
  artist_counts = pd.Series(artists).value_counts()
  artist_counts = artist_counts.reset_index()
  artist_counts = artist_counts.rename(columns={"index": "Artist", 0: "Count"})
  artist_counts = artist_counts.to_dict(orient='records')

  results6 = db.session.query(Albums.year).filter(Albums.album_id == Album_Genres.album_id).filter(Album_Genres.genre_id == Genres.genre_id).filter(Genres.name == genre).all()
  years = [str(result[0]) for result in results6]
  year_counts = pd.Series(years).value_counts()
  year_counts = year_counts.reset_index()
  year_counts = year_counts.rename(columns={"index": "Year", 0: "Associated_Count"})
  year_counts = year_counts.sort_values(by=["Year"])

  year_totals = []
  for unique_year in year_counts["Year"]:
    year_results = db.session.query(Albums.year).filter(Albums.year == unique_year).filter(Genres.name == assoc_genre).all()
    year_total_count = len(year_results)
    year_totals.append(year_total_count)

  year_counts["Total_Count"] = year_totals
  year_counts = year_counts.sort_values(by=["Associated_Count"], ascending=False)
  year_counts = year_counts.to_dict(orient='records')

  data = {
    "Genre": name, 
    "Description": description, 
    "Album_Count": album_count, 
    "Associated_Genre_Counts": assoc_genre_counts, 
    "Random_Covers": random_covers, 
    "Label_Counts": label_counts, 
    "Artist_Counts": artist_counts, 
    "Year_Counts": year_counts,
    }
  return jsonify(data)

@app.route("/api/genre_associations")
def genre_associations_api():
  results = db.session.query(Genres.name).all()
  genres = [result[0] for result in results]
  
  genres = list(set(genres))
  genres.sort()

  data = []
  for genre in genres:
    genre_dict = {"Genre": genre}
    results = db.session.query(Album_Genres.album_id).filter(Album_Genres.genre_id == Genres.genre_id).filter(Genres.name == genre).all()
    album_ids = [result[0] for result in results]
    genre_total_album_count = [len(album_ids)]
    genre_dict["Total_Count"] = genre_total_album_count
    
    results1 = db.session.query(Genres.name).filter(Genres.genre_id == Album_Genres.genre_id).filter(Album_Genres.album_id.in_(album_ids))
    assoc_genres = [result[0] for result in results1]
    assoc_genre_counts = pd.Series(assoc_genres).value_counts()
    assoc_genre_counts = assoc_genre_counts.reset_index()
    assoc_genre_counts = assoc_genre_counts.rename(columns={"index": "Genre", 0: "Associated_Count"})
    assoc_genre_counts = assoc_genre_counts.sort_values(by=["Genre"])
    
    assoc_genre_totals = []
    for assoc_genre in assoc_genre_counts["Genre"]:
      results2 = db.session.query(Album_Genres.album_id).filter(Album_Genres.genre_id == Genres.genre_id).filter(Genres.name == assoc_genre).all()
      album_ids = [result[0] for result in results2]
      assoc_genre_total_album_count = len(album_ids)
      assoc_genre_totals.append(assoc_genre_total_album_count)
    
    assoc_genre_counts["Total_Count"] = assoc_genre_totals
    genre_dict["Associated_Genres"] = assoc_genre_counts.to_dict(orient='records')
    data.append(genre_dict)

  return jsonify(data)


if __name__ == "__main__":
  app.run(debug=True)
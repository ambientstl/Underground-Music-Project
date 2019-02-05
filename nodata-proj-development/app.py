from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo
import random

app = Flask(__name__)

#connect to mongo and retrieve data
mongo = PyMongo(app, uri="mongodb://localhost:27017/underground_music_db")
nodataInfo = mongo.db.nodata_db.find()

#clean data
cleanNodata = []
for data in nodataInfo:
  data.pop('_id')
  cleanNodata.append(data)

#home route
@app.route("/")
def home():
  return render_template("index.html")

#test image links
#######remove s from https during scrapes
@app.route("/testpics")
def testpics():
  pics = []
  randNodata = random.sample(cleanNodata, 9)
  # return jsonify(cleanNodata)
  for album in randNodata:
    pic = album["cover"]
    pic = pic.replace("s", "", 1)
    pics.append(pic)

  return render_template("index1.html", pics=pics)

####################
#### API ROUTES ####
####################

#all albums
@app.route("/api/albums")
def test():
  return jsonify(cleanNodata)

#all values for key (artist, label, year, genres)
@app.route("/api/<key>")
def arb_key(key):
  #set empty data dictionary
  data = {key: []}
  #set empty set
  uniqueData = set()
  #set empty genre list
  genreList = []
  #if key = artist/label/year
  if key == "artist" or key == "label" or key == "year":
    #for each album
    for album in cleanNodata:
      #set value of key
      value = album[key]
      #add to set to keep only unique values
      uniqueData.add(value)
    #append unique list to data dict
    data[key].append(list(uniqueData))
  #if key = genres
  elif key == "genres":
    #for each album
    for album in cleanNodata:
      #set value of key
      value = album[key]
      #for each tag in list
      for entry in value:
        #append to genre list
        genreList.append(entry)
    #genre list into unique genre set
    genres = set(genreList)
    #append list of genres to data dict
    data[key].append(list(genres))
  else:
    #key error message
    return jsonify({"Key Error": (f"'{key}' not valid. Use 'artist', 'genres', 'label', or 'year'")}), 404
  #return data dict
  return jsonify(data)

#all albums with key+value (artist, label, year, genres)
##########strip whitespace from artist and album during scrape # album[key] = album[key].strip()
##########TODO: convert search and value to same format
@app.route("/api/<key>/<value>")
def arb_key_value(key, value):
  #set data dict
  data = {"albums": []}
  #if key = artist/label/year
  if key == "artist" or key == "label" or key == "year":
    #for each album
    for album in cleanNodata:
      #if key's value = input value
      if album[key] == value:
        #append album to data dict
        data["albums"].append(album)
      #else do nothing
      else:
        ""
    #return data dict
    return jsonify(data)
  #if key = genres
  elif  key == "genres":
    # if "+" in value:
    #   albums = []
    #   inputGenres = value.split("+")
    #   for album in cleanNodata:
    #     for genre in inputGenres:
    #       if genre in album[key]:
    #         albums.append(album)
    #       else:
    #         ""
    #   #################
    #   ##this needs work
    #   uniqueAlbums = set(albums)
    #   albumList = list(uniqueAlbums)
    #   data["albums"].append(albumList)
    #   return jsonify(data)
    # else:
    for album in cleanNodata:
      if value in album[key]:
        data["albums"].append(album)
      else:
        ""
    return jsonify(data)
  else:
    return jsonify({"error": (f"Album(s) with key '{key}' and value '{value}' not found.")}), 404
  









# @app.route("/<key>/<value>")
# def nodata_arb_key_value(key, value):
#   for album in nodataInfo:
#     if album[key] == value:
#       return jsonify(album)

#     return jsonify({"error": f"Album with key {key} and value {value} not found."}), 404

# @app.route("/api/<key>")
# #for artist, year, genre, and label
# def api_arb_key(key):
#   #set empty dict
#   info = {key: }
#   #for album in db
#   for album in nodataInfo:
#     #find value of key
#     value = album[key]
#     #if value in info already, 
#     if value in info[key]:
#       #do nothing
#     #else, append the value
#     else: info[key].append(value)
#   #returns jsonified list of values for key
#   return jsonify(info)

# @app.route("/api/<key>/<value>")
# #for artist, year, genre*, and label
# def api_arb_key_value(key, value):
#   #if key is genre,
#   if key == "genre":
#     #and if + in value
#     if "+" in value:
#       #split search at +
#       genres = value.split("+")

#       #set empty dict
#       info = {[]}
#       #for album in db
#       for album in nodataInfo:
#         #if genres are in album's genre list,
#         if album["genre"] == genre[0] & genre[1]:
#           #add album to list
#           info.append(album)
        


  
#   #set empty dict
#   info = {[]}
#   #for album in db
#   for album in nodataInfo:
#     #if key and value match,
#     if album[key] == value:
#       #add to dict
#       info.append(album)
#   #return jsonified list of albums with key/value match 
#   return jsonify(info)


if __name__ == "__main__":
    app.run(debug=True)
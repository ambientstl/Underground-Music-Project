# Underground-Music-Project
Collecting and analyzing data scraped from underground music blog nodata.tv

1. run Scrape&CreateDB-Development.ipynb to scrape 1 page of albums into a mongo db
2. run app.py to launch a Flask app
3. routes: 
* / -home page
* /testpics -9 random album covers from the db
* /api/albums -json list of all albums in db
* <keys>: artist, genres, label, year
* /api/<key> -json list of all values for key
* /api/<key>/<value> -json list of all albums with that key-value pair

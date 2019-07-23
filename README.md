# Underground-Music-Project
Collecting and analyzing data scraped from underground music blog nodata.tv

1. run CreateDB.py to scrape 2,000 albums into a mySQL database
      - to scrape less albums (and cut down on scraping time), reduce the range on line 41 in CreateDB.py
2. create config.py and set "mySQLpassword" to your root password
3. run app.py, and visit http://127.0.0.1:5000/
3. routes: 
```
* / -home page: album count graph and genre summaries
* /genres -list of genres
* /genre/<genre> -information about the genre
* /api -lists available api routes
```

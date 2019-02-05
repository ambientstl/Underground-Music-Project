function unpack(rows, index) {
  return rows.map(function(row) {
    return row[index];
  });
}
albums = []
artists = []
labels = []
catalogs = []
years = []
urls = []
function getAllAlbumData() {

  var queryUrl = '/api/albums';
  d3.json(queryUrl).then(function(data) {
    data.forEach(album => {
      albums.append(album.album)

    });
    buildTable(albums, artists, labels, catalogs, years, urls);
  });
}

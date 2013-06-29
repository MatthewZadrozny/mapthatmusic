import urllib
import random

ID_LENGTH = 22

def getTrackID(location):
	#process the location for web requests
	processedLocation = process(location)

	#get albumid
	albumid = getAlbumID(location)

	#lookup album by id in spotify
	f = urllib.urlopen("http://ws.spotify.com/lookup/1/?uri=spotify:album:" + albumid + "&extras=track")
	response = f.read()
	f.close()

	#get all tracks on that album
	tracks = response.split("track href=\"spotify:track:")[1:]

	#pick a track, get its id
	track = tracks[random.randint(0, len(tracks)-1)]
	trackid = track[: ID_LENGTH]

	return trackid

def getAlbumID(location):
	#get artistid
	artistid = getArtistID(location)

	#lookup artist by id in spotify
	f = urllib.urlopen("http://ws.spotify.com/lookup/1/?uri=spotify:artist:" + artistid + "&extras=album")
	response = f.read()
	f.close()

	#get all albums by that artist
	albums = response.split("album href=\"spotify:album:")[1:]

	#pick an album, find its id
	album = albums[random.randint(0, len(albums)-1)]
	albumid = album[:ID_LENGTH]

	return albumid


def getArtistID(location):
	artists = getArtists(location)
	artistids = []
	for artist in artists:
		#search for artist in spotify
		f = urllib.urlopen("http://ws.spotify.com/search/1/artist?q=" + artist)
		response = f.read()
		f.close()

		#parse response to get artist id
		correctName = response.find(">" + artist + "<")

		if correctName != -1:
			idLoc = correctName - 12 - ID_LENGTH
			artistids.append(response[idLoc : idLoc + ID_LENGTH])
	return artistids[random.randint(0, len(artistids)-1)]

def getArtists(location):
	#get response from echo nest
	f = urllib.urlopen("http://developer.echonest.com/api/v4/artist/search?api_key=8GBMBBXYRRNW35FQB&format=json&artist_location=" + location + "&bucket=artist_location")
	response = f.read()
	f.close()

	#fetch list of names from response
	names = [nameString[: nameString.find('"')] for nameString in response.split('"name": "')]

	return names

def process(location):
	#replace spaces with pluses for web request
	processedLocation = ""
	for word in location.split(" "):
		processedLocation += word + "+"
	processedLocation = processedLocation[:-1]

	return processedLocation

print getTrackID("united sates")

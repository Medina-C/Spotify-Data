import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

scopes = "playlist-read-private playlist-read-collaborative"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scopes))

# TO INCLUDE: 
#album, main artist, all artists, duration, name, popularity, item number
#end time, end date, ms listened
#danceability, energy, key?, loudness, speechiness, acousticness, instrumentalness, liveness, valence, tempo, time signature, mode (major or minor), 

def main():
    print("Enter file path for streaming history JSON file: ")
    baseData = getBaseData()
    baseData = [baseData[0]]
    data = {}

    trackIds = [] # List to later group search the audio features

    # Search each item and save useful data
    for i, item in enumerate(baseData):
    
        query = 'track:"{name}" artist:"{artist}"'.format(
            name = item['trackName'], artist = item['artistName'])
        
        result = sp.search(q=query, market = 'CA', type = 'track')

        track = result['tracks']['items'][0] # Assume the first result is the right one

        trackIds.append(track['id'])

        data[i] = {}
        data[i]['Title'] = track['name']
        data[i]['Time Listened'] = item['msPlayed']
        data[i]['Listen Date'] = item['endTime'].split(' ')[0]
        data[i]['End Time'] = item['endTime'].split(' ')[1]
        data[i]['Principal Artist'] = track['artists'][0]['name']
        data[i]['All Artists'] = getArtists(track)
        data[i]['Album'] = track['album']['name']
        data[i]['Track Number'] = track['track_number']
        data[i]['Length'] = track['duration_ms']
        data[i]['Popularity'] = track['popularity']
   

# Get the data from the original Streaming History json file provided
def getBaseData():
    
    filePath = input()

    if filePath == "":
        print('Program terminated.')
        exit()

    filePath = filePath.replace('\\', '/')

    try:
        with open(filePath, encoding = 'utf8') as file:
            return json.load(file)
    except:
        print('File not found. Try again or hit enter to cancel.')
        return getBaseData()

# Get all artists for a track
def getArtists(track):
    artists = []
    for artist in track['artists']:
        artists.append(artist['name'])
    return artists


main()
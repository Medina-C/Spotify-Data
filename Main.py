import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

scopes = "playlist-read-private playlist-read-collaborative"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scopes))

def main():
    print("Enter file path for streaming history JSON file: ")

    data = getBaseData()

    track = data[0]
    
    query = 'track:"{name}" artist:"{artist}"'.format(
        name = track['trackName'], artist = track['artistName'])
    
    result = sp.search(q=query, market = 'CA')

    trackId = result['tracks']['items'][0]['id']
    
    #album, artists, duration, name, popularity, track number
    #danceability, energy, key?, loudness, speechiness, acousticness, instrumentalness, liveness, valence, tempo, time signature, mode (major or minor), 

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


main()
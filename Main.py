import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import math

scopes = "playlist-read-private playlist-read-collaborative"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scopes))

# TO INCLUDE: 
#album, main artist, all artists, duration, name, popularity, item number
#end time, end date, ms listened
#danceability, energy, key, loudness, speechiness, acousticness, instrumentalness, valence, tempo, time signature, mode (major or minor), 
#TODO handle songs that cannot be found
#TODO check if songs have already been queried to save time

def main():
    print("Enter file path for streaming history JSON file: ")
    baseData = getBaseData()
    data = {}

    trackIds = [] # List to later group search the audio features

    # Search each item and save useful data
    for i, item in enumerate(baseData):
        print('Querying ', item['trackName'])

        query = 'track:"{name}" artist:"{artist}"'.format(
            name = item['trackName'], artist = item['artistName'])
        
        result = sp.search(q=query, market = 'CA', type = 'track')
        
        if len(result['tracks']['items']) < 1:
            query = '"{name}"'.format(name = item['trackName'])
            result = sp.search(q=query, market = 'CA', type = 'track')

            if len(result['tracks']['items']) < 1:
                print('Song {name} by {artist} could not be found. Aborting program.').format(
                    name = item['trackName'], artist = item['artistName'])
                exit()

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

    # Get the audio features in groups of 100
    hundreds = math.ceil(len(trackIds)/100)

    for i in range(hundreds):
        group = get100Group(trackIds, i)
        features = sp.audio_features(group)

        for j, item in enumerate(features):
            track = data[i*100 + j]

            track['Danceability'] = item['danceability']
            track['Energy'] = item['energy']
            track['Key'] = keyToString(item['key'])
            track['Loudness'] = item['loudness']
            track['Mode'] = modeToString(item['mode'])
            track['Speechiness'] = item['speechiness']
            track['Acousticness'] = item['acousticness']
            track['Instrumentalness'] = item['instrumentalness']
            track['Positivity'] = item['valence']
            track['Tempo'] = item['tempo']
            track['Time Signature'] = item['time_signature']


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

# Gets the groupNumth group of 100 items in the list
def get100Group(list, groupNum):
    result = []
    for i in range(100):
        index = groupNum*100 + i

        if index >= len(list):
            return result
        
        result.append(list[index])

    return result

def keyToString(key):
    return {
        0: 'C',
        1: 'C#/Db', 
        2: 'D',
        3: 'D#/Eb',
        4: 'E',
        5: 'F',
        6: 'F#/Gb',
        7: 'G',
        8: 'G#/Ab',
        9: 'A',
        10: 'A#/Bb',
        11: 'B'
    }[key]

def modeToString(mode):
    if mode == 1:
        return 'Major'
    else:
        return 'Minor'

main()
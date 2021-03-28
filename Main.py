import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import math
import xlsxwriter
from dotenv import load_dotenv

load_dotenv()
scopes = "playlist-read-private playlist-read-collaborative"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scopes))

# TO INCLUDE: 
#album, main artist, duration, name, popularity, item number
#end time, end date, ms listened
#danceability, energy, key, loudness, speechiness, acousticness, instrumentalness, valence, tempo, time signature, mode (major or minor), 
#TODO handle if spreadsheet is already open
#TODO genre and playlist

def main():
    print("Enter file path for streaming history JSON file: ")

    baseData, filePath = getBaseData()
    data = []

    trackIds = {} # List to later group search the audio features

    # baseData2 = [baseData[i] for i in range(10)]
    # baseData = baseData2
    print('Working... (May take several minutes)')
    # Search each item and save useful data
    for i, item in enumerate(baseData):
  
        track = checkAlready(data, item)
        alreadyThere = track is not None

        data.append({})
        if alreadyThere:
            track = track.copy()
            data[i] = track
            trackIds[(track['Title'], track['Artist'])]['array'].append(i)
        else:
            query = 'track:"{name}" artist:"{artist}"'.format(
                name = item['trackName'], artist = item['artistName'])
            
            result = search(query)
            
            if len(result['tracks']['items']) < 1:
                query = '"{name}"'.format(name = item['trackName'])
                result = sp.search(q=query, market = 'CA', type = 'track')

                if len(result['tracks']['items']) < 1:
                    print('Song {name} by {artist} could not be found. Skipping.'.format(
                        name = item['trackName'], artist = item['artistName']))
                    continue

            track = result['tracks']['items'][0] # Assume the first result is the right one
            
            trackIds[(item['trackName'], track['artists'][0]['name'])] = {
                'id': track['id'],
                'array': [i]
            }
        
        data[i]['Title'] = item['trackName']
        data[i]['Time Listened'] = item['msPlayed']
        data[i]['Listen Date'] = item['endTime'].split(' ')[0]
        data[i]['End Time'] = item['endTime'].split(' ')[1]

        if not alreadyThere:
            data[i]['Artist'] = track['artists'][0]['name']
            data[i]['Album'] = track['album']['name']
            data[i]['Track Number'] = track['track_number']
            data[i]['Length'] = track['duration_ms']
            data[i]['Popularity'] = track['popularity']
    
    # Get the audio features in groups of 100
    hundreds = math.ceil(len(list(trackIds.values()))/100)
    for i in range(hundreds):
        
        idList = list(trackIds.values())
        group = get100Group(idList, i)
        features = sp.audio_features(group)

        for j, featureSet in enumerate(features):
            for index in idList[i*100 + j]['array']:

                data[index]['Danceability'] = featureSet['danceability']
                data[index]['Energy'] = featureSet['energy']
                data[index]['Key'] = keyToString(featureSet['key'])
                data[index]['Loudness'] = featureSet['loudness']
                data[index]['Mode'] = modeToString(featureSet['mode'])
                data[index]['Speechiness'] = featureSet['speechiness']
                data[index]['Acousticness'] = featureSet['acousticness']
                data[index]['Instrumentalness'] = featureSet['instrumentalness']
                data[index]['Positivity'] = featureSet['valence']
                data[index]['Tempo'] = featureSet['tempo']
                data[index]['Time Signature'] = featureSet['time_signature']

    # Export data
    newPath = filePath.split('.json')[0] + ' UPGRADED.xlsx'
    workbook = xlsxwriter.Workbook(newPath)
    sheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True})

    keys = data[0].keys()
    sheet.write_row(0, 0, keys, bold)

    for i, item in enumerate(data):
        sheet.write_row(i+1, 0, item.values())

    workbook.close()
    print('Complete!')

# Get the data from the original Streaming History json file provided
def getBaseData():
    filePath = input()

    if filePath == "":
        print('Program terminated.')
        exit()

    filePath = filePath.replace('\\', '/')

    if filePath[0] == '"' and filePath[len(filePath)-1 == '"']:
        filePath = filePath[1:len(filePath)-1]

    try:
        with open(filePath, encoding = 'utf8') as file:
            return json.load(file), filePath
    except:
        print('File not found. Try again or hit enter to cancel.')
        return getBaseData()

# Gets the groupNumth group of 100 items in the list
def get100Group(list, groupNum):
    result = []
    for i in range(100):
        index = groupNum*100 + i

        if index >= len(list):
            return result
        
        result.append(list[index]['id'])

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

def search(query):
    try:
        return sp.search(q=query, market = 'CA', type = 'track')
    except:
        print("ERROR - trying again")
        search(query)

# Check if that song has already been queried
def checkAlready(data, check):
    for track in data:
        try:
            if track['Title'] == check['trackName'] and track['Artist'] == check['artistName']:
                return track
        except KeyError:
            continue

main()
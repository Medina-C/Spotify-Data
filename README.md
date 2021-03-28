# Spotify-Data

Expands the base streaming history data provided when you download your Spotify data.

## Setup

You need to create an app on Spotify's developer website and add the app's IDs to this program for it to work.

1. Follow the steps in [these instructions](https://developer.spotify.com/documentation/general/guides/app-settings/) to create an app and set the redirect uri (I use `http://localhost:8888/callback` which works fine).
2. Edit the **.env** file and insert your client ID, client secret, and redirect uri in between the quotations.

## Running the app

1. When it prompts you, paste in the file path to the **StreamingHistory0.json** file in provided when you download your Spotify data. Include the file name in the path. It's okay if the pasted path contains double backslashes instead of a single forward slash, or if it starts and ends with quotations. If it says, "file not found," you probably put the path in wrong.
2. The program will run through every song in that file. If it can't find something (it won't find podcasts, for example) it will output a message and skip that item.
3. It will take several minutes to complete. It will print a message when done.
4. When finished, it will output a csv file with all of your data.

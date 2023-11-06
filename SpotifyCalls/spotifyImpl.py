import spotipy
import credentials as cred
from spotipy.oauth2 import SpotifyOAuth
import json
import time

#Scope for testing purposes of API calls and rate limit testing
scope = ["user-read-recently-played","user-modify-playback-state","user-read-currently-playing"]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.CLIENT_ID, client_secret=cred.CLIENT_SECRET, redirect_uri=cred.REDIRECT_URI,scope=scope))  
  
results = sp.current_user_recently_played()

#getting users 50 most recently played tracks
tracklist = []
for idx, item in enumerate(results['items']):
    track = item['track']
    tracklist.append(track)

# Adding sample tracks to queue
# for i in range(20,25):
#     sp.add_to_queue(tracklist[i]['uri'])
#     print(str(tracklist[i]['name'])+" has been added to the queue")

track = sp.currently_playing()

# Code to test playback control
# print('Skipping to track: ' + tracklist[23]['name'])
# while track['item']['name'] != tracklist[23]['name']:
#     track = sp.currently_playing()
#     print("Current playing: " + track['item']['name'])
#     if track['item']['name'] == tracklist[23]['name']:
#         break
#     time.sleep(2)
#     sp.next_track()


recGenres = ['classical','pop','rock']
recs = sp.recommendations(seed_genres=recGenres, limit=3)
data = json.dumps(recs,indent=2)
print(data)
print("\n\nRecommendations"+
        "\n-----------------------------------------------")
#Displaying the recommendations that were generated
recTracklist = []
for i in recs["tracks"]:
    artists = i['artists'][0]['name']
    track = i['name']

    print(artists + " - " + track)    
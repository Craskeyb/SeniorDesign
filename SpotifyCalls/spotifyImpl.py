import spotipy
import credentials as cred
from spotipy.oauth2 import SpotifyOAuth
import time

#Scope for actual implementation of playback control
#scope = ["user-read-playback-state","user-modify-playback-state"]

#Scope for testing purposes of API calls and rate limit testing
scope = ["user-read-recently-played","user-modify-playback-state","user-read-currently-playing"]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.CLIENT_ID, client_secret=cred.CLIENT_SECRET, redirect_uri=cred.REDIRECT_URI,scope=scope))  
  
results = sp.current_user_recently_played()

#getting users 50 most recently played tracks
tracklist = []
for idx, item in enumerate(results['items']):
    track = item['track']
    tracklist.append(track)


for i in range(10,15):
    sp.add_to_queue(tracklist[i]['uri'])
    print(str(tracklist[i]['name'])+" has been added to the queue")

track = sp.currently_playing()

if track['item']['name'] != tracklist[10]['name']:
    sp.next_track()
    track = sp.currently_playing()
    time.sleep(2)

#Extracting artists, track names, and genres from the api response to seed the recommendation generator
# recArtists = []
# recTracks = []
# recGenres = ['classical','hip-hop','r&b','rap']
# for i in range(10,19):
#     if tracklist[i]['uri'] not in recTracks:
#         recTracks.append(tracklist[i]['uri'])
#     if tracklist[i]['artists'] not in recArtists:
#         recArtists.append(tracklist[i]['artists'])

# artistsURI = []
# for artist in recArtists:
#     if artist[0]['uri'] not in artistsURI:
#         artistsURI.append(artist[0]['uri'])


# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.CLIENT_ID, client_secret=cred.CLIENT_SECRET, redirect_uri=cred.REDIRECT_URI,scope=scope))  

# recs = sp.recommendations(seed_tracks=recTracks[0],seed_genres=recGenres,seed_artists=artistsURI[0], limit=10)

# print("\n\nRecommendations based on 10 of your top tracks"+
#         "\n-----------------------------------------------")
# #Displaying the recommendations that were generated
# recTracklist = []
# for idx,item in enumerate(recs['items']):
#     track = item['track']
    
#     artists = track['artists']
#     trackname = track['name']

#     print(str(trackname) + " - " + artists)
    
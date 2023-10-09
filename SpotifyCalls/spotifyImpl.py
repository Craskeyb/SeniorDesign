import spotipy
import credentials as cred
from spotipy.oauth2 import SpotifyOAuth

#Scope for actual implementation of playback control
#scope = ["user-read-playback-state","user-modify-playback-state"]

#Scope for testing purposes of API calls and rate limit testing
scope = "user-read-recently-played"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.CLIENT_ID, client_secret=cred.CLIENT_SECRET, redirect_uri=cred.REDIRECT_URI,scope=scope))  
  
# access_token = sp_oauth.get_access_token()  
# refresh_token = sp_oauth.get_refresh_token()  

results = sp.current_user_recently_played()

for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])
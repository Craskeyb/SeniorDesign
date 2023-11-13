import spotipy
import SongSelect.SpotifyCalls.credentials as cred
from spotipy.oauth2 import SpotifyOAuth
import json
import time

#Class for generating an instance of the Spotipy API Application
class RecGenerator:
    def __init(self):
        #Scope for testing purposes of API calls and rate limit testing
        scope = ["user-read-recently-played","user-modify-playback-state","user-read-currently-playing"]

        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.CLIENT_ID, client_secret=cred.CLIENT_SECRET, redirect_uri=cred.REDIRECT_URI,scope=scope))  


    #Recommendation Method
    def makeRecommendation(self, genre):
        recs = self.sp.recommendations(seed_genres=genre, limit=10)
        data = json.dumps(recs,indent=2)
        print(data)
        print("\n\nRecommendations"+
                "\n-----------------------------------------------")
        #Displaying the recommendations that were generated
        for i in recs["tracks"]:
            artists = i['artists'][0]['name']
            track = i['name']

            print(artists + " - " + track)  

        self.sp.add_to_queue(recs["tracks"][0])
        self.sp.next_track()  
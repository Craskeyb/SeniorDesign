import spotipy
import SongSelect.SpotifyCalls.credentials as cred
from spotipy.oauth2 import SpotifyOAuth
import json
import time

#Class for generating an instance of the Spotipy API Application
class RecGenerator:
    def __init__(self):
        #Scope for testing purposes of API calls and rate limit testing
        scope = ["user-read-recently-played","user-modify-playback-state","user-read-currently-playing"]

        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.CLIENT_ID, client_secret=cred.CLIENT_SECRET, redirect_uri=cred.REDIRECT_URI,scope=scope))  

        #Internal variable to keep track of the songs that have been played already to avoid repeats
        self.played = []

    #Recommendation Method
    def makeRecommendation(self, genre):
        #Get recommendations from Spotify API
        recs = self.sp.recommendations(seed_genres=genre, limit=10)

        #API Call to determine what genres can be used for recommendations
        ### USED FOR TESTING ###
        #available_genres = self.sp.recommendation_genre_seeds()
        # print(available_genres)

        # Converting data to clean json for ease of viewing
        ### USED FOR TESTING ###
        # data = json.dumps(recs,indent=2)
        # print(data)

        #Getting the recommendations that match our tempo evaluation
        songInfo = []
        for song in recs["tracks"]:
            songInfo.append(self.sp.audio_features(song["uri"])[0]["tempo"])

        print(songInfo)

        print("\n\nRecommendations"+
                "\n-----------------------------------------------")
        #Displaying the recommendations that were generated
        for i in recs["tracks"]:
            artists = i['artists'][0]['name']
            track = i['name']

            print(artists + " - " + track)  

        self.sp.add_to_queue(recs["tracks"][0]["uri"])
        self.sp.next_track()  
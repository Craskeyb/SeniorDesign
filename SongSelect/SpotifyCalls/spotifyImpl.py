import spotipy
import SongSelect.SpotifyCalls.credentials as cred
from spotipy.oauth2 import SpotifyOAuth
import statistics
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
    def makeRecommendation(self, genre, motion):
        #Get recommendations from Spotify API
        recs = self.sp.recommendations(seed_genres=genre, limit=15)

        #API Call to determine what genres can be used for recommendations
        ### USED FOR TESTING ###
        #available_genres = self.sp.recommendation_genre_seeds()
        # print(available_genres)

        # Converting data to clean json for ease of viewing
        ### USED FOR TESTING ###
        # data = json.dumps(recs,indent=2)
        # print(data)

        #Getting the tempos of each song to choose recs based on motion
        songTempos = []
        for song in recs["tracks"]:
            songTempos.append(self.sp.audio_features(song["uri"])[0]["tempo"])
        
        print("Song Tempos:")
        print(songTempos)

        #After getting tempos, choose the songs that best fit based on amount of motion
        prunedRecs = []
        if motion == 'High':
            while len(prunedRecs) < 3: #If high motion, take the 3 highest tempos from the recs
                prunedRecs.append(recs["tracks"][songTempos.index(max(songTempos))])
                songTempos[songTempos.index(max(songTempos))] = 0 #Set val to zero to avoid double selection
        elif motion == 'Medium':
            while len(prunedRecs) < 3: #If medium, take the 3 median values from the recs
                prunedRecs.append(recs["tracks"][songTempos.index(statistics.median(songTempos))])
                songTempos[songTempos.index(statistics.median(songTempos))] = 0 #Set val to zero to avoid double selection
        else:
            while len(prunedRecs) < 3: #If low, take the 3 min values from the recs
                prunedRecs.append(recs["tracks"][songTempos.index(min(songTempos))])
                songTempos[songTempos.index(min(songTempos))] = 10**5 #Set value at index of min to be very high so it is not selected twice


        print("\n\nRecommendations"+
                "\n-----------------------------------------------")
        #Displaying the recommendations that were generated
        for i in recs["tracks"]:
            artists = i['artists'][0]['name']
            track = i['name']

            print(artists + " - " + track) 

        print("\n\nRecommendations Chosen based on "+ motion + " motion level" +
                "\n-----------------------------------------------")
        #Displaying the 3 recs chosen to be queued based on motion
        for rec in prunedRecs:
            artist = rec['artists'][0]['name']
            track = rec['name']
            print(artist + " - " + track)
        
        #Queueing the pruned songs
        self.sp.add_to_queue(prunedRecs[0]["uri"])  
        self.sp.add_to_queue(prunedRecs[1]["uri"])
        self.sp.add_to_queue(prunedRecs[2]["uri"])
        self.skipToNew(prunedRecs)

    
    #Function to skip to recently queued songs
    def skipToNew(self, prunedRecs):
        while self.sp.currently_playing()['item']['name'] != prunedRecs[0]['name']:
            time.sleep(2)
            self.sp.next_track()
            

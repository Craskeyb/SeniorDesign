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

    #Recommendation Method
    def makeRecommendation(self, genre, motion, n):
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

        #After getting tempos, choose the n best songs that best fit based on amount of motion
        prunedRecs = []
        if motion == 'High':
            while len(prunedRecs) < n: #If high motion, take the n highest tempos from the recs
                prunedRecs.append(recs["tracks"][songTempos.index(max(songTempos))])
                songTempos[songTempos.index(max(songTempos))] = 0 #Set val to zero to avoid double selection
        elif motion == 'Medium':
            while len(prunedRecs) < n: #If medium, take the n median values from the recs
                prunedRecs.append(recs["tracks"][songTempos.index(statistics.median(songTempos))])
                songTempos[songTempos.index(statistics.median(songTempos))] = 0 #Set val to zero to avoid double selection
        else:
            while len(prunedRecs) < n: #If low, take the n min values from the recs
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
        #Displaying the n recs chosen to be queued based on motion
        for rec in prunedRecs:
            artist = rec['artists'][0]['name']
            track = rec['name']
            print(artist + " - " + track)
            time.sleep(2)
            self.sp.add_to_queue(rec["uri"])
        
        time.sleep(1)
        self.skipToNew(prunedRecs)

    
    #Function to skip to recently queued songs
    def skipToNew(self, prunedRecs):
        while self.sp.currently_playing()['item']['name'] != prunedRecs[0]['name']:
            time.sleep(1)
            self.sp.next_track()
            self.sp.pause_playback()
            time.sleep(1)

        self.sp.start_playback()

    #Function to check the current length of the queue to determine how many songs need to be queued
    def getQueueLen(self):
        return len(self.sp.queue())
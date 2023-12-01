from SongSelect.decTree import decTree
from SongSelect.SpotifyCalls.spotifyImpl import RecGenerator
from SongSelect.testRowGenerator import rowGenerator
from ComputerVision.ComputerVision import ComputerVision
import sys
import matplotlib.pyplot as plt
import time

class AiDj():
    def __init__(self):
        print("******************************")
        print("* Welcome to the Live AI DJ! *")
        print("******************************\n")
        print("Initializing components...")
        
        #Keep track of latency in class instantiation, and begin timing for end-to-end latency
        start = time.time()
        self.e2eStart = start 
        self.decisionTree = decTree()
        self.computer_vision = ComputerVision()

        #Instantiate the Spotify API Application
        self.songRecs = RecGenerator()
        end = time.time()
        runtime_ms = (end-start)*1000
        self.initialRun = True
        print("All components ready in " + str(runtime_ms) + "ms\n\n")

    def liveAiDj(self):
        #Restart e2e latency timer if on a subsequent run
        if self.e2eStart == 0:
            self.e2eStart = time.time()
            self.initialRun = False

        #Perform a prediction based on input data (hardcoded for now)
        #Take note of latency for data retrieval
        start = time.time()
        (data, motion) = self.computer_vision.get_data()
        end = time.time()
        runtime_ms = (end-start)*1000
        print("Data retrieved in " + str(runtime_ms) + "ms\n\n")
        #Perform a prediction based on random synthetic input data
        # (data, motion) = rowGenerator()

        print(data)

        predStart = time.time()
        prediction = self.decisionTree.giniPrediction(data)
        # prediction = self.decisionTree.giniPrediction([[10,0,0,0,1,0,0,0,20.11,200]])
        predEnd = time.time()

        predRuntime_ms = (predEnd-predStart)*1000
        print("\nGini prediction for input data: " + prediction)
        print("\nPrediction generated in " + str(predRuntime_ms) + "ms")


        #Evaluate the prediction using the methods found in predictionEval.py
        evalStart = time.time()

        #decisionTree.evaluatePrediction([10,0,0,0,1,0,0,0,20.11,120], prediction)
        emoteScore, inputScore, scenScore = self.decisionTree.evaluatePrediction(data.iloc[0], prediction)
        
        #Calculate latency for the prediction evaluation
        evalEnd = time.time()
        evalRuntime_ms = (evalEnd - evalStart)*1000
        print('\nPrediction evaluation complete in ' + str(evalRuntime_ms) + 'ms')
        
        #Print result of the prediction evaluation
        if emoteScore*100//1 > 85 and inputScore*100//1 > 60 and scenScore*100//1 > 40:
            print("Good recommendation, appending to training set")
        else:
            print("Bad recommendation, re-requesting data for new prediction")

        #Make recommendation based on prediction & motion, and record latency
        recStart = time.time()
        self.songRecs.makeRecommendation(prediction, motion,3)
        recEnd = time.time()
        self.e2eEnd = recEnd 
        
        recRuntime_ms = (recEnd - recStart)*1000
        print("\nRecommendation complete in " + str(recRuntime_ms) + "ms")
        
        if self.initialRun == True:
            self.e2eRuntime_ms = (self.e2eEnd - self.e2eStart)*1000
            print("\nEnd-to-end runtime from startup to generation of first rec: " + str(self.e2eRuntime_ms) + "ms")
        else:
            self.e2eRuntime_ms = (self.e2eEnd - self.e2eStart)*1000
            print("\nEnd-to-end runtime for subsequent: " + str(self.e2eRuntime_ms) + "ms")

        self.e2eStart = 0

        #TODO: write logic + loop to check the # of songs in queue, and if its less than 3 queue until there are 3



    def testSynthetic(self):
        #Instantiate a new decision tree object
        decisionTree = decTree()

        #Perform test of large synthetic data set utilizing randomly chosen input rows
        decisionTree.testSyntheticData()



if __name__ == "__main__":
    # liveAiDj()
    aidj = AiDj()

    while(True):
        print('--------------------------------------------------')
        cmd = input('Press enter to process or type \'exit\' to end: ')
        if cmd == 'exit':
            sys.exit()
        plt.close('all')

        try:
            aidj.liveAiDj()
        except Exception as error:
            print("Error Occurred. Try again")
            print("ERROR: ", error)
        # aidj.decisionTree.plotTree()
    #testSynthetic()
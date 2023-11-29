from SongSelect.decTree import decTree
from SongSelect.SpotifyCalls.spotifyImpl import RecGenerator
from SongSelect.testRowGenerator import rowGenerator
from ComputerVision.ComputerVision import ComputerVision
import sys
import matplotlib.pyplot as plt

class AiDj():
    def __init__(self):
        print("******************************")
        print("* Welcome to the Live AI DJ! *")
        print("******************************\n")
        print("Initializing components...")
        self.decisionTree = decTree()
        self.computer_vision = ComputerVision()
        print("All components ready\n\n")

        #Instantiate the Spotify API Application
        self.songRecs = RecGenerator()

    def liveAiDj(self):
        #Instantiate a new decision tree object

        #Perform a prediction based on input data (hardcoded for now)
        (data, motion) = self.computer_vision.get_data()

        #Perform a prediction based on random synthetic input data
        # (data, motion) = rowGenerator()

        print(data)

        # prediction = self.decisionTree.giniPrediction(data)
        prediction = self.decisionTree.giniPrediction([[10,0,0,0,1,0,0,0,20.11,200]])
        print("\nGini prediction for input data: " + prediction)

        #Evaluate the prediction using the methods found in predictionEval.py
        #decisionTree.evaluatePrediction([10,0,0,0,1,0,0,0,20.11,120], prediction)
        emoteScore, inputScore, scenScore = self.decisionTree.evaluatePrediction(data.iloc[0], prediction)
        if emoteScore*100//1 > 85 and inputScore*100//1 > 60 and scenScore*100//1 > 40:
            print("Good recommendation, appending to training set")
        else:
            print("Bad recommendation, re-requesting data for new prediction")
        
        self.songRecs.makeRecommendation(prediction, motion)


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
        except:
            print("Error Occurred. Try again")
        # aidj.decisionTree.plotTree()
    #testSynthetic()
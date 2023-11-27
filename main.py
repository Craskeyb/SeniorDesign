from SongSelect.decTree import decTree
from SongSelect.SpotifyCalls.spotifyImpl import RecGenerator
from ComputerVision.ComputerVision import ComputerVision
import sys

class AiDj():
    def __init__(self):
        print("******************************")
        print("* Welcome to the Live AI DJ! *")
        print("******************************\n")
        print("Initializing components...")
        self.decisionTree = decTree()
        self.computer_vision = ComputerVision()

    def liveAiDj(self):
        #Instantiate a new decision tree object

        #Perform a prediction based on input data (hardcoded for now)
        (data, motion) = self.computer_vision.get_data()

        print(data)

        prediction = self.decisionTree.giniPrediction(data)
        # prediction = decisionTree.giniPrediction([[10,0,0,0,1,0,0,0,20.11,120]])
        print("\nGini prediction for input data: " + prediction)

        #Evaluate the prediction using the methods found in predictionEval.py
        #decisionTree.evaluatePrediction([10,0,0,0,1,0,0,0,20.11,120], prediction)
        self.decisionTree.evaluatePrediction(data.iloc[0], prediction)

        #Instantiate the Spotify API Application
        songRecs = RecGenerator()
        songRecs.makeRecommendation(prediction)

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
    
        aidj.liveAiDj()
    #testSynthetic()
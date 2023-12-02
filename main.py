from SongSelect.decTree import decTree
from SongSelect.SpotifyCalls.spotifyImpl import RecGenerator
from SongSelect.testRowGenerator import rowGenerator
from ComputerVision.ComputerVision import ComputerVision
import sys
import matplotlib.pyplot as plt
import time
import csv

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

        #Keep track of the number of predictions, as well as the amount of 'good' predictions
        self.iterations = 0
        self.goodRecs = 0
        self.latencyTimes = []

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

        currentLatencies = {}

        #Perform a prediction based on input data (hardcoded for now)
        #Take note of latency for data retrieval
        start = time.time()
        (data, motion) = self.computer_vision.get_data()
        end = time.time()
        runtime_ms = (end-start)*1000
        currentLatencies['CV'] = runtime_ms
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

        currentLatencies['ML'] = predRuntime_ms

        #Evaluate the prediction using the methods found in predictionEval.py
        evalStart = time.time()

        #decisionTree.evaluatePrediction([10,0,0,0,1,0,0,0,20.11,120], prediction)
        emoteScore, inputScore, scenScore = self.decisionTree.evaluatePrediction(data.iloc[0], prediction)
        
        #Calculate latency for the prediction evaluation
        evalEnd = time.time()
        evalRuntime_ms = (evalEnd - evalStart)*1000
        print('\nPrediction evaluation complete in ' + str(evalRuntime_ms) + 'ms')
        
        currentLatencies['Eval'] = evalRuntime_ms

        #Print result of the prediction evaluation
        # if emoteScore*100//1 > 85 and inputScore*100//1 > 60 and scenScore*100//1 > 40:
        if emoteScore*100//1 > 70 and inputScore*100//1 > 40 and scenScore*100//1 > 50:
            print("Good recommendation, appending to training set")
            self.goodRecs += 1
            data=data.assign(genre=[prediction[0]])
            data.to_csv('Datasets\\reinforcementTrainingData.csv', mode='a', index=False, header=False)
        else:
            print("Bad recommendation, will be ignored for training set")

        #Make recommendation based on prediction & motion, and record latency
        recStart = time.time()
        if self.iterations == 0:
            self.prunedRecs = self.songRecs.makeRecommendation(prediction, motion, 3)
            self.songRecs.skipToNew(self.prunedRecs)
        else:
            self.prunedRecs = self.songRecs.makeRecommendation(prediction, motion, 3 - self.songRecs.getQueueLen(self.prunedRecs[-1]['name']))
        recEnd = time.time()
        self.e2eEnd = recEnd 
        
        recRuntime_ms = (recEnd - recStart)*1000
        print("\nRecommendation complete in " + str(recRuntime_ms) + "ms")
        
        currentLatencies['Spotify'] = recRuntime_ms

        if self.initialRun == True:
            self.e2eRuntime_ms = (self.e2eEnd - self.e2eStart)*1000
            print("\nEnd-to-end runtime from startup to generation of first rec: " + str(self.e2eRuntime_ms) + "ms")
            currentLatencies['E2E'] = self.e2eRuntime_ms
        else:
            self.e2eRuntime_ms = (self.e2eEnd - self.e2eStart)*1000
            print("\nEnd-to-end runtime for subsequent: " + str(self.e2eRuntime_ms) + "ms")
            currentLatencies['E2E'] = self.e2eRuntime_ms

        self.latencyTimes.append(currentLatencies)
        print(len(self.latencyTimes))
        self.e2eStart = 0

        self.iterations += 1




    def testSynthetic(self):
        #Instantiate a new decision tree object
        decisionTree = decTree()

        #Perform test of large synthetic data set utilizing randomly chosen input rows
        decisionTree.testSyntheticData()
    
    def generatePerformanceData(self):
        fName = 'performanceData' + str(time.time()) + '.txt'
        performanceFile = open(fName, "w")
        performanceFile.write("Performance Data for Recent Session with Live AI DJ"+
                              "\n---------------------------------------------------\n")
        performanceFile.write("Total number of predictions made: " + str(self.iterations) + 
                              "\nGood predictions (appended to training data): " + str(self.goodRecs) +  
                              "\nPercentage of good predictions: " + str(((self.goodRecs/self.iterations)*100)//1))
        
        #Now calculating latencies and adding them to the performance file
        avgCV = 0
        avgML = 0
        avgEval = 0
        avgSpotify = 0
        avgE2E = 0
        fName = 'latencyData' + str(time.time()) + '.csv'
        with open(fName, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['CV', 'ML', 'Eval', 'Spotify', 'E2E'])
            
            for trials in self.latencyTimes:
                avgCV+=trials['CV']
                avgML+=trials['ML']
                avgEval+=trials['Eval']
                avgSpotify+=trials['Spotify']
                avgE2E+=trials['E2E']

                writer.writerow([trials['CV'], trials['ML'], trials['Eval'], trials['Spotify'], trials['E2E']])
        
        performanceFile.write("\n\nLatency Data (in milliseconds)" + 
                              "\n------------------\n")
        
        performanceFile.write("Average latency for Computer Vision module: " + str(avgCV/len(self.latencyTimes))+
                              "\nAverage latency for Machine Learning predictions: " + str(avgML/len(self.latencyTimes))+ 
                              "\nAverage latency for prediction evaluation function: " + str(avgEval/len(self.latencyTimes))+
                              "\nAverage latency for Spotify API calls: " + str(avgSpotify/len(self.latencyTimes))+
                              "\nAverage end-to-end runtime for program: " + str(avgE2E/len(self.latencyTimes))+
                              "\n\nComplete latency data for each function can be found in \'latencyData.csv\'")

        
        



if __name__ == "__main__":
    # liveAiDj()
    aidj = AiDj()

    try:
        while(True):
            if aidj.iterations == 0:
                try:
                    aidj.liveAiDj()
                except Exception as error:
                    print("Error Occurred. Try again")
                    print("ERROR: ", error)
            if aidj.songRecs.getQueueLen(aidj.prunedRecs[-1]['name']) < 3:
                print('--------------------------------------------------')
                # cmd = input('Press enter to process or type \'exit\' to end: ')
                # if cmd == 'exit':
                #     aidj.generatePerformanceData()
                #     sys.exit()
                plt.close('all')

                try:
                    aidj.liveAiDj()
                except Exception as error:
                    print("Error Occurred. Try again")
                    print("ERROR: ", error)
            # aidj.decisionTree.plotTree()
            time.sleep(30)
    except KeyboardInterrupt:
        aidj.generatePerformanceData()
        sys.exit()




    #testSynthetic()
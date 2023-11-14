# Song Selection ML Algorithm #
import pandas as pd
import random
from sklearn.metrics import confusion_matrix 
from sklearn.model_selection import train_test_split 
from sklearn.tree import DecisionTreeClassifier 
from sklearn import tree
from sklearn.metrics import accuracy_score 
import matplotlib.pyplot as plt
import statistics
from SongSelect import predictionEval

class decTree:
    def __init__(self):
        #First, import the data from the training data file (will be using example data)
        self.inputData = pd.read_csv('Datasets\\trainingData.csv')

        #Reading in the data we want to predict from
        self.cleanInput = self.inputData.loc[:,~self.inputData.columns.isin(['genre'])]

        #Training the models on initialization to be used by the predictive functions later on
        self.entropyModel = self.entropyTrain(self.cleanInput.values, self.inputData['genre'])
        self.giniModel = self.giniTrain(self.cleanInput.values, self.inputData['genre'])


    #Function for training the model based on entropy
    def entropyTrain(self, input, output):
        #Implement fitting data to model using entropy as primary training criterion
        # Decision tree with entropy 
        clf_entropy = DecisionTreeClassifier( 
                criterion = "entropy", random_state = 100, 
                max_depth = 5, min_samples_leaf = 5) 
    
        # Performing training 
        clf_entropy.fit(input, output) 
        return clf_entropy 

    #Function for training the model based on Gini Index
    def giniTrain(self, input, output):
        #Implement fitting data to model using gini index as primary training criterion
        # Creating the classifier object 
        clf_gini = DecisionTreeClassifier(criterion = "gini", 
                random_state = 100,max_depth= 5, min_samples_leaf=5) 
    
        # Performing training 
        clf_gini.fit(input, output)
        return clf_gini

    #Function to test the data with randomly selected synthetic test values generated with the test set generator script
    def testSyntheticData(self):
        print("-- Running prediction tests on large set of synthetic data values --")

        #Reading in test data from generated file and removing genre for input to decision tree model
        testData = pd.read_csv('Datasets\\testData.csv')
        cleanTest = testData.loc[:,~testData.columns.isin(['genre'])]

        #Randomly selecting rows from the test file to make predictions from
        testIdx = []
        while len(testIdx) < 300:
            num = random.randint(0,len(cleanTest)-1)
            if num not in testIdx:
                testIdx.append(num)
        
        #Getting the outputs from the test data to compare the predictions to
        testArr = []
        outputCheck = []
        for num in testIdx:
            testArr.append(cleanTest.iloc[num])
            outputCheck.append(testData.iloc[num]['genre'])


        #entropyPred = self.prediction(testArr, self.entropyModel)
        giniPred = self.prediction(testArr, self.giniModel)

        #entropyAcc = accuracy_score(entropyPred, outputCheck)
        giniAcc = accuracy_score(giniPred, outputCheck)

        #print("\nEntropy Prediction Accuracy: " + str(entropyAcc*100//1) + "%")
        print("Gini Prediction Accuracy: " + str(giniAcc*100//1) + "%")

        #entCheck = []
        giniCheck = []
        for val in testArr[0]:
            #entCheck.append(val)
            giniCheck.append(val)
        
        #print("\nEvaluating entropy predictions")
        #self.evaluateSyntheticPredictions(testArr,entropyPred)

        print("\nEvaluating gini predictions")
        self.evaluateSyntheticPredictions(testArr,giniPred)
        


    #Function to make a prediction based on a decision tree model that is passed in
    #Version of function for internal use, requires input of decision tree object
    def prediction(self, testData, decTree):
        #Calling the predict function for the decision tree object
        pred = decTree.predict(testData)
        return pred

    #Function for external use that utilizes the Gini Index-based decision tree model
    def giniPrediction(self, testData):
        #Calling the predict function for the decision tree object
        pred = self.giniModel.predict(testData)
        return pred
    
    #Function for external use that utilizes the Entropy-based decision tree model
    def entropyPrediction(self, testData):
        #Calling the predict function for the decision tree object
        pred = self.entropyModel.predict(testData)
        return pred
    
    #Function to check the accuracy of a prediction based on the developed criteria
    def evaluatePrediction(self, testData, prediction):
        emotionScore, inputScore = predictionEval.similarityScore(testData, prediction, self.inputData)
        scenarioScore = predictionEval.scenarioScore(testData, prediction)

        print("\nEmotion similarity: " + str(emotionScore*100//1) + "%")
        print("Input similarity: " + str(inputScore*100//1) + "%")

        print("Scenario Score: " + str(scenarioScore*100//1) + "%")

    #Function to perform the prediction evaluation for the whole set of test data (performs on every row, and averages the result)
    def evaluateSyntheticPredictions(self, testData, prediction):
        emotionArr = []
        inputArr = []
        scenarioArr = []
        for i in range(len(prediction)):
            emScore,inScore = predictionEval.similarityScore(testData[i],prediction[i],self.inputData)
            emotionArr.append(emScore)
            inputArr.append(inScore)
            scenarioArr.append(predictionEval.scenarioScore(testData[i],prediction[i]))
        
        print("\nAverage values across all test predictions")
        print("-------------------------------------------")
        print("Average emotion similarity: " + str(statistics.mean(emotionArr)*100//1))
        print("Average input similarity: " + str(statistics.mean(inputArr)*100//1))
        print("Average scenario score: " + str(statistics.mean(scenarioArr)*100//1))

    #Function to generate and display a visualization of the tree, which includes the splitting criteria at each node
    def plotTree(self, decTree):
        # Plotting visualization of tree
        plt.figure(figsize=(20,10))
        tree.plot_tree(decTree)
        plt.show()

    
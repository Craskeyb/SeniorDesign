# Song Selection ML Algorithm #

import pandas as pd
#import numpy as np
import random
from sklearn.metrics import confusion_matrix 
from sklearn.model_selection import train_test_split 
from sklearn.tree import DecisionTreeClassifier 
from sklearn.metrics import accuracy_score 
#from sklearn.metrics import classification_report

def entropyTrain(input, output):
    #Implement fitting data to model using entropy as primary training criterion
    print("Training with Entropy")
    # Decision tree with entropy 
    clf_entropy = DecisionTreeClassifier( 
            criterion = "entropy", random_state = 100, 
            max_depth = 3, min_samples_leaf = 5) 
  
    # Performing training 
    clf_entropy.fit(input, output) 
    return clf_entropy 

def giniTrain(input, output):
    #Implement fitting data to model using gini index as primary training criterion
    print("Training with Gini Index")
    # Creating the classifier object 
    clf_gini = DecisionTreeClassifier(criterion = "gini", 
            random_state = 100,max_depth=3, min_samples_leaf=5) 
  
    # Performing training 
    clf_gini.fit(input, output) 
    return clf_gini


def prediction(testData, decTree):

    pred = decTree.predict(testData)
    print("Classifier Prediction: ")
    print(pred)
    return pred

def main():
    #First, import the data from the test file (will be using example data)
    data = pd.read_csv('Datasets\IRIS.csv')

    #Reading in the data we want to predict from
    inputData = pd.read_csv('Datasets\IRIS.csv')
    cleanInput = inputData.loc[:,~data.columns.isin(['species'])]

    testIdx = []
    while len(testIdx) < 15:
        num = random.randint(0,len(cleanInput)-1)
        if num not in testIdx:
            testIdx.append(num)
    
    testArr = []
    outputCheck = []
    for num in testIdx:
        testArr.append(cleanInput.iloc[num])
        outputCheck.append(inputData.iloc[num]['species'])

    entropyModel = entropyTrain(cleanInput, inputData['species'])
    giniModel = giniTrain(cleanInput, inputData['species'])

    entropyPred = prediction(testArr, entropyModel)
    giniPred = prediction(testArr, giniModel)

    entropyAcc = accuracy_score(entropyPred, outputCheck)
    giniAcc = accuracy_score(giniPred, outputCheck)

    print("Entropy Prediction Accuracy: " + str(entropyAcc*100//1) + "%")
    print("Gini Prediction Accuracy: " + str(giniAcc*100//1) + "%")

if __name__ == "__main__":
    main()
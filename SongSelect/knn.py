import math
import numpy as np
import pandas as pd


#Function for calculating distance using various strategies
def distance(trained, test, style) -> float:

    dist = 0.0

    if(style == 'euc'):
        #First strategy: normal euclidean distance: sqrt(sum i to N(x1_i-x2_i)^2)
        #Stopping at len(row)-1 because we don't want to include the output (last column) in this calculation
        for i in range(len(trained)-1):
            dist += (trained[i]-test[i])**2
        dist = math.sqrt(dist)

    #Second strategy: Manhattan Distance (sum of differences)
    elif(style == 'man'):
        for i in range(len(trained)-1):
            dist += abs(trained[i]-test[i])

    #Third strategy: Minkowski distance (combination of euclidean & manhattan)
    elif(style == 'mink'):
        #1 indicates manhattan, 2 is for euclidean
        p = 1
        for i in range(len(trained)-1):
            dist += abs(trained[i]-test[i])**p
        dist = dist**(1/p)

    #TODO: Implement Hamming Distance somehow if categorical variables are needed in the input data?
        #Hamming distance: check for difference in categories, distance is 0 if same, can be weighted to different values if not

    return dist

#Function for getting the k nearest neighbors based on the test data
def knnPrediction(trainedData, testData, k):
    
    neigh = {}
    for row in trainedData.iterrows():
        dist = distance(row[1],testData,"mink")
        neigh[dist] = row
    
    sortedNeighbors = sorted(neigh.keys())

    kClosest = []

    for key in sortedNeighbors:
        if len(kClosest) < k:
            kClosest.append(neigh[key][1])
        else:
            break
    
    classifiers = [label['species'] for label in kClosest]
    prediction = max(set(classifiers), key=classifiers.count)

    return prediction
                    
            
#First, import the data from the test file (will be using example data)
#Will be replaced by HTTP requests in future iterations
data = pd.read_csv('Datasets\IRIS.csv')

#Reading in the data we want to predict from
inputData = pd.read_csv('Datasets\IRIS.csv')

outputCheck = inputData['species']
cleanInput = inputData.loc[:,~data.columns.isin(['species'])]

#Number of neighbors we want to check for our prediction
k = 3
correctCount = 0
for i in range(len(cleanInput)):
    testOutput = knnPrediction(data,cleanInput.iloc[i],k)
    print("The prediction for row " + str(i) + " of the test data is classified as: " + testOutput)
    if(testOutput == outputCheck[i]):
        correctCount += 1
    
print("\n\nThe percentage of correct predictions is " + str(correctCount*100//len(cleanInput)) + "%")
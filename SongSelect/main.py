from decTree import decTree

def liveAiDj():
    #Instantiate a new decision tree object
    decisionTree = decTree()

    #Perform test of large synthetic data set utilizing randomly chosen input rows
    #decisionTree.testSyntheticData()

    #Perform a prediction based on input data (hardcoded for now)
    prediction = decisionTree.giniPrediction([[10,0,0,0,1,0,0,0,20.11,120]])
    print("\nGini prediction for input data: " + prediction)

    #Evaluate the prediction using the methods found in predictionEval.py
    decisionTree.evaluatePrediction([[10,0,0,0,1,0,0,0,20.11,120]], prediction)


if __name__ == "__main__":
    liveAiDj()
import statistics
import numpy as np
import pandas as pd
from SongSelect import knn

def similarityScore(test, prediction, train):
    neighbors = knn.kNearest(train, test, prediction, 5)
    #test = test[0:-2]
    
    
    emotionSim = []
    emTemp = []
    inputSim = []
    inputTemp = []
    for neigh in neighbors:
        neigh = neigh[0:-2]
        for i in range(len(neigh)-1):
            if 1 <= i <= 7:
                #Calculate Similarity for classifiers - Hamming Distance Check
                if neigh[i] == test[i]:
                    emTemp.append(1)
                else:
                    emTemp.append(0)
            else:
                #Calculate Similarity for continuous vals - Percent Difference from Training Data
                inputTemp.append(1-abs(neigh[i]-test[i])/neigh[i])
        
        emotionSim.append(emTemp.count(1)/len(emTemp))
        inputSim.append(statistics.mean(inputTemp))

    return statistics.mean(emotionSim), statistics.mean(inputSim)


def scenarioScore(test, prediction):
    ### Light Ranges
    ### Direct Light: 220-255
    ### Regularly Lit: 180 - 220
    ### Dimly Lit: 80 - 180
    ### Dark: 18 - 80
    rockLight = (255 + 180)/2
    popLight = (80+220)/2
    elecLight = (18+180)/2
    metalLight = (18+180)/2
    classicalLight = (220+180)/2
    jazzLight = (18+180)/2
    darkLight = (18+80)/2

    ### Temp Ranges
    ### Hot: 22.9 - 24.4
    ### Room Temp: 19.5 - 22.8
    ### Cold: 17.2 - 19.4
    rockTemp = (20+24.4)/2
    popTemp = (21+24.4)/2
    elecTemp = (22+24.4)/2
    metalTemp = (22 +24.4)/2
    classicalTemp = (17.2+21)/2
    jazzTemp = (17.2+22.8)/2
    darkTemp = (17.2+20)/2

    ### Count Ranges (Roughly)
    ### Densely Populated: 20+
    ### Moderately Populated: 10-19
    ### Lightly Populated: 5-9
    ### Low Population: 1-4
    rockCount = 12.5
    popCount = 12.5
    elecCount = 12.5
    metalCount = 12.5
    classicalCount = 10
    jazzCount = 10
    darkCount = 5

    ### Emotion/Genre Correlations (angry disgust fear happy neutral sad surprise)
    ### Rock - Angry, Happy
    ### Pop - Happy, Surprised
    ### Electronic - Happy, Surprised
    ### Metal - Angry, Disgust, Scared
    ### Jazz - Neutral, Happy
    ### Classical - Neutral, Sad
    ### Dark Ambient - Scared, Disgust, Sad
    rockEmote = [1,0,0,1,0,0,0]
    popEmote = [0,0,0,1,0,0,1]
    elecEmote = [0,0,0,1,0,0,1]
    metalEmote = [1,1,1,0,0,0,0]
    jazzEmote = [0,0,0,1,1,0,0]
    classicalEmote = [0,0,0,0,1,0,0]
    darkEmote = [0,1,1,0,0,1,0]

    ### Genre Scenarios (Subject to Adjustment based on Testing Data)
    
    ### Rock 
    ### Light - Regular->Bright
    ### Emotions - Happy, Angry
    ### Temperature - High Room Temp -> Hot
    ### Count - Light -> Dense

    ### Pop
    ### Light - Dim -> Regular
    ### Emotions - Happy, Surprised
    ### Temperature - Room Temp -> Hot
    ### Count - Light -> Dense

    ### Electronic
    ### Light - Dark -> Dim
    ### Emotions - Happy, Surprised
    ### Temperature - High Room Temp -> Hot
    ### Count - Light -> Dense

    ### Metal 
    ### Light - Dark -> Dim
    ### Emotions - Angry, Disgust, Scared
    ### Temperature - High Room Temp -> Hot
    ### Count - Light -> Dense

    ### Jazz 
    ### Light - Dark -> Dim
    ### Emotions - Neutral, Happy
    ### Temperature - Cold -> Room Temp
    ### Count - Low -> Moderate

    ### Classical 
    ### Light - Any
    ### Emotions - Neutral, Sad
    ### Temperature - Cold -> Room Temp
    ### Count - Low -> Dense

    ### Dark Ambient 
    ### Light - Dark -> Dim
    ### Emotions - Sad, Angry, Disgust
    ### Temperature - Cold -> Room Temp
    ### Count - Low -> Light

    #First, evaluate which scenario the prediction falls in
    #Next, evaluate how close to the center of the scenario ranges the value falls
    scoreArr = [0]*10
    if prediction == 'rock':
        #Count
        scoreArr[0] = 1-abs((rockCount-test[0])/rockCount)
        
        #Emotion
        for i in range(1,7):
            if test[i] == rockEmote[i]:
                scoreArr[i] = 1
        
        #Temp
        scoreArr[8] = 1 - abs((rockTemp-test[8])/rockTemp)
        
        #Light
        scoreArr[9] = 1-abs((rockLight-test[0])/rockLight)

    elif prediction == 'pop':
        #Count
        scoreArr[0] = 1-abs((popCount-test[0])/popCount)
        
        #Emotion
        for i in range(1,7):
            if test[i] == popEmote[i]:
                scoreArr[i] = 1
        
        #Temp
        scoreArr[8] = 1 - abs((popTemp-test[8])/popTemp)
        
        #Light
        scoreArr[9] = 1-abs((popLight-test[0])/popLight)

    elif prediction == 'electronic':
        #Count
        scoreArr[0] = 1-abs((elecCount-test[0])/elecCount)
        
        #Emotion
        for i in range(1,7):
            if test[i] == elecEmote[i]:
                scoreArr[i] = 1
        
        #Temp
        scoreArr[8] = 1 - abs((elecTemp-test[8])/elecTemp)
        
        #Light
        scoreArr[9] = 1-abs((elecLight-test[0])/elecLight)
    
    elif prediction == 'metal':
        #Count
        scoreArr[0] = 1-abs((metalCount-test[0])/metalCount)
        
        #Emotion
        for i in range(1,7):
            if test[i] == metalEmote[i]:
                scoreArr[i] = 1
        
        #Temp
        scoreArr[8] = 1 - abs((metalTemp-test[8])/metalTemp)
        
        #Light
        scoreArr[9] = 1-abs((metalLight-test[0])/metalLight)
    
    elif prediction == 'classical':
        #Count
        scoreArr[0] = 1-abs((classicalCount-test[0])/classicalCount)
        
        #Emotion
        for i in range(1,7):
            if test[i] == classicalEmote[i]:
                scoreArr[i] = 1
        
        #Temp
        scoreArr[8] = 1 - abs((classicalTemp-test[8])/classicalTemp)
        
        #Light
        scoreArr[9] = 1-abs((classicalLight-test[0])/classicalLight)
     
    elif prediction == 'jazz':
        #Count
        scoreArr[0] = 1-abs((jazzCount-test[0])/jazzCount)
        
        #Emotion
        for i in range(1,7):
            if test[i] == jazzEmote[i]:
                scoreArr[i] = 1
        
        #Temp
        scoreArr[8] = 1 - abs((jazzTemp-test[8])/jazzTemp)
        
        #Light
        scoreArr[9] = 1-abs((jazzLight-test[0])/jazzLight)
    
    else:
        #Count
        scoreArr[0] = 1-abs((darkCount-test[0])/darkCount)
        
        #Emotion
        for i in range(1,7):
            if test[i] == darkEmote[i]:
                scoreArr[i] = 1
        
        #Temp
        scoreArr[8] = 1 - abs((darkTemp-test[8])/darkTemp)
        
        #Light
        scoreArr[9] = 1-abs((darkLight-test[0])/darkLight)

    return statistics.mean(scoreArr)
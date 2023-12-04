import csv
import numpy as np
import pandas as pd
#from SongSelect.decTree import decTree
#from SongSelect.testRowGenerator import rowGenerator
import random

def refineDataset():
    deciTree = decTree()
    goodRecs = 0
    iterations = 100
    #Loop through iterations of random rows, and check the scores to determine if it should be appended to the training set
    for i in range(iterations):
        (data, motion) = rowGenerator()
        prediction = deciTree.giniPrediction(data.values)
        emoteScore, inputScore, scenScore = deciTree.evaluatePrediction(data.iloc[0],prediction)
        data=data.assign(genre=[prediction[0]])
        #Print result of the prediction evaluation
        if emoteScore*100//1 > 70 and inputScore*100//1 > 40 and scenScore*100//1 > 50:
            goodRecs += 1
            data.to_csv('Datasets\\reinforcementTrainingData.csv', mode='a', index=False, header=False)


    print("Out of " + str(iterations) + " iterations, " + str((goodRecs/iterations)*100) + " were good")

def createDataset():
    # Define the possible values for each column
    numrows = 250
    genres = ['rock', 'pop', 'jazz', 'metal', 'electronic', 'classical', 'sad']
    count_values = list(range(1, 21))
    emotion_values = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
    temperature_values = [round(random.uniform(17, 26), 2) for _ in range(700)]
    light_values = [random.randint(30, 200) for _ in range(550)] + [random.randint(196, 220) for _ in range(150)]

    rockEmote = [1,0,0,1,0,0,0]
    popEmote = [0,0,0,1,0,0,1]
    elecEmote = [0,0,0,1,0,0,1]
    metalEmote = [1,1,1,0,0,0,0]
    jazzEmote = [0,0,0,1,1,0,0]
    classicalEmote = [0,0,0,0,1,0,0]
    sadEmote = [0,1,1,0,0,1,0]


    # Create and populate the CSV file
    with open('Datasets\\reinforcementTrainingData.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['count', 'angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise', 'temperature', 'light', 'genre'])
        for genre in genres: 
            for _ in range(numrows):
                if genre == 'rock':
                    emoteBool = rockEmote
                    randCount = random.choice(list(range(5,20)))
                    randTemp = random.choice(list(np.arange(20,24.4, 0.2)))
                    randLight = random.choice(list(range(180,255)))
                elif genre == 'pop':
                    emoteBool = popEmote
                    randCount = random.choice(list(range(5,20)))
                    randTemp = random.choice(list(np.arange(21,24.4, 0.2)))
                    randLight = random.choice(list(range(80,220)))
                elif genre == 'jazz':
                    emoteBool = jazzEmote
                    randCount = random.choice(list(range(3,17)))
                    randTemp = random.choice(list(np.arange(17.2,22.8, 0.2)))
                    randLight = random.choice(list(range(18,180)))
                elif genre == 'metal':
                    emoteBool = metalEmote
                    randCount = random.choice(list(range(5,20)))
                    randTemp = random.choice(list(np.arange(22,24.4, 0.2)))
                    randLight = random.choice(list(range(18,180)))
                elif genre == 'electronic':
                    emoteBool = elecEmote
                    randCount = random.choice(list(range(5,20)))
                    randTemp = random.choice(list(np.arange(22,24.4, 0.2)))
                    randLight = random.choice(list(range(18,180)))
                elif genre == 'classical':
                    emoteBool = classicalEmote
                    randCount = random.choice(list(range(2,15)))
                    randTemp = random.choice(list(np.arange(17.2,21, 0.2)))
                    randLight = random.choice(list(range(180,220)))
                else:
                    emoteBool = sadEmote
                    randCount = random.choice(list(range(1,6)))
                    randTemp = random.choice(list(np.arange(17.2,20, 0.2)))
                    randLight = random.choice(list(range(18,80)))
                writer.writerow([
                    randCount,
                    emoteBool[0],emoteBool[1],emoteBool[2],emoteBool[3],emoteBool[4],emoteBool[5],emoteBool[6],
                    randTemp,
                    randLight,
                    genre
                ])

if __name__ == "__main__":
    createDataset()
    #refineDataset()
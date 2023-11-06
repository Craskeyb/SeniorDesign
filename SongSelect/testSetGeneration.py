import random
import csv

#Define function to pick genre for training set based on combination of inputs
def genreChoice(count,emote,temp,light) -> str:
    if emote == 'angry':
        if light < 196:
            return 'metal'
        else:
            return 'rock'
    elif emote == 'surprise':
        if count > 5:
            return 'electronic'
        else:
            return 'pop'
    elif emote == 'sad':
        if light > 196:
            return 'classical'
        else:
            return 'dark ambient'
    elif emote == 'neutral':
        if count > 6:
            return 'jazz'
        else:
            return 'classical'
    elif emote == 'disgust':
        if count > 10 and temp > 22:
            return 'metal'
        else:
            return 'rock'
    elif emote == 'happy':
        if light < 196 and count > 10:
            return 'disco'
        else:
            return 'pop'
    else:
        if count < 10:
            return 'dark ambient'
        else:
            return 'rock'

# Define the possible values for each column
count_values = list(range(1, 21))
emotion_values = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
emotion_count = [0]*7
temperature_values = [round(random.uniform(18, 30), 2) for _ in range(700)]
light_values = [random.randint(30, 220) for _ in range(700)]


# Create and populate the CSV file
with open('Datasets\\testData.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['count', 'angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral', 'temperature', 'light', 'genre'])
    for _ in range(700):
        emote = random.choice(emotion_values)
        emoteBool = [0]*7
        if emote == 'angry':
            emotion_count[0]+=1
            emoteBool[0] = 1
        elif emote == 'disgust':
            emotion_count[1]+=1
            emoteBool[1] = 1
        elif emote == 'fear':
            emotion_count[2]+=1
            emoteBool[2] = 1
        elif emote == 'happy':
            emotion_count[3]+=1
            emoteBool[3] = 1
        elif emote == 'sad':
            emotion_count[4]+=1
            emoteBool[4] = 1
        elif emote == 'surprise':
            emotion_count[5]+=1
            emoteBool[5] = 1
        else:
            emotion_count[6]+=1
            emoteBool[6] = 1
        
        for i in range(len(emotion_values),-1):
            if emotion_count[i] == 100:
                emotion_values.pop(i)
                emotion_count.pop(i)

        randCount = random.choice(count_values)
        randTemp = random.choice(temperature_values)
        randLight = random.choice(light_values)
        writer.writerow([
            randCount,
            emoteBool[0],emoteBool[1],emoteBool[2],emoteBool[3],emoteBool[4],emoteBool[5],emoteBool[6],
            randTemp,
            randLight,
            genreChoice(randCount,emotion_values[emoteBool.index(1)],randTemp,randLight)
        ])
        


print("CSV file 'testData.csv' has been created.")

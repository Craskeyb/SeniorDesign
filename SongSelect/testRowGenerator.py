import random
import pandas as pd

def rowGenerator():

    # Define the possible values for each column
    count_values = list(range(1, 21))
    emotion_values = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
    emoteDict = {'angry':0,'disgust':0,'fear':0,'happy':0,'neutral':0,'sad':0,'surprise':0}
    temperature_values = [round(random.uniform(17, 30), 2) for _ in range(700)]
    light_values = list(range(30,220))

    data = {}

    data["count"] = random.choice(count_values)

    emote = random.choice(emotion_values)
    emoteDict[emote] = 1
    data.update(emoteDict)

    randTemp = random.choice(temperature_values)
    randLight = random.choice(light_values)
    sensorDict = {'temperature':randTemp,'light':randLight}
    data.update(sensorDict)

    return pd.DataFrame([data])



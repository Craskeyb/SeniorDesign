import random
import pandas as pd

def rowGenerator():

    # Define the possible values for each column
    count_values = list(range(1, 21))
    emotion_values = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
    emotion_count = [0]*7
    temperature_values = [round(random.uniform(17, 30), 2) for _ in range(700)]
    light_values = list(range(30,220))

    data = {}

    randCount = random.choice(count_values)
    randTemp = random.choice(temperature_values)
    randLight = random.choice(light_values)
import tensorflow as tf
import os
import numpy as np


class EmotionDetection():
    def __init__(self):
        self.model = tf.keras.models.load_model('emotion_recognition_model_5.keras')
        pass
    
    def classify(self):
        emotions = {}
        class_names = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
        emotions = dict.fromkeys(class_names, None)
        
        for images in os.listdir('faces'):
            print(images)
            img = tf.keras.utils.load_img('faces\\'+images, target_size=(48, 48))
            img_array = tf.keras.utils.img_to_array(img)
            img_array = tf.expand_dims(img_array, 0)

            predictions = self.model.predict(img_array)
            score = tf.nn.softmax(predictions[0])
            emotion = class_names[np.argmax(score)]
            print(
                images + " most likely belongs to {} with a {:.2f} percent confidence."
                .format(emotion, 100 * np.max(score))
            )

            if emotions[emotion] is not None:
                emotions[emotion] += 1
            else:
                emotions[emotion] = 1

            print(score)
        return emotions
    
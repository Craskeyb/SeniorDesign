import tensorflow as tf
import os
import numpy as np
import matplotlib.pyplot as plt
import cv2


class EmotionDetection():
    
    """
    Constructor to initialize the emotion detection CNN model
    """
    def __init__(self):
        tf.get_logger().setLevel('ERROR')
        self.model = tf.keras.models.load_model('ComputerVision\\emotion_recognition_model_5.keras')
        self.class_names =  ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
        pass
    
    """
    Classifies all of the images in the ComputerVision/Faces directory using the CNN model

    Returns:

    """
    def classify(self):
        emotions = {}
        emotions = dict.fromkeys(self.class_names, None)

        imgnum = 1
        num_imgs = len(os.listdir('ComputerVision\\faces'))
        plt.figure("Emotions")
        
        for images in os.listdir('ComputerVision\\faces'):
            oimg = cv2.imread('ComputerVision\\faces\\' + images)
            img = tf.keras.utils.load_img('ComputerVision\\faces\\'+images, target_size=(48, 48))
            img_array = tf.keras.utils.img_to_array(img)
            img_array = tf.expand_dims(img_array, 0)

            predictions = self.model.predict(img_array, verbose=0)
            score = tf.nn.softmax(predictions[0])
            emotion = self.class_names[np.argmax(score)]
            print(
                images + " is {} with a {:.2f} percent confidence."
                .format(emotion, 100 * np.max(score))
            )

            if emotions[emotion] is not None:
                emotions[emotion] += 1
            else:
                emotions[emotion] = 1

            self.plot_prediction(images, oimg, score.numpy().tolist(), emotion, imgnum, num_imgs)
            imgnum += 2
        plt.show(block=False)
        plt.savefig('emotionDetection.jpg')
        return emotions
    
    def plot_prediction(self, name, image, scores, emotion, im_num, num_images):
        plt.subplot(num_images,2,im_num)
        plt.grid(False)
        plt.xticks([])
        plt.yticks([])
        plt.imshow(image)
        plt.xlabel(emotion + " " +  str(100*np.max(scores)))

        plt.subplot(num_images,2,im_num+1)
        plt.grid(False)
        plt.xticks(np.arange(7), ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise'], rotation=90)
        plt.yticks([])
        plt.ylim([0,1])
        bar_plt = plt.bar(range(7), scores)
        plt.bar_label(bar_plt, fmt='%.2f')
    
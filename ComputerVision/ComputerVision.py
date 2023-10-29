import FaceCount
import FaceExtraction
import EmotionDetection
import cv2
import sys
import os
import pandas as pd

class ComputerVision:
    def __init__(self):
        self.face_count = FaceCount.FaceCount()
        self.face_extraction = FaceExtraction.FaceExtraction()
        self.emotion_detection = EmotionDetection.EmotionDetection()
    
    def get_face_count(self, image):
        count = self.face_count.get_face_count(image)

        print(count, " faces detected")
        return count
    
    def extract_faces(self, image):
        count = self.face_extraction.extract_faces(image)

        print(count, " faces extracted")

    def get_emotion(self):
        # TODO: Get inferences on each face from trained CNN
        emotions = self.emotion_detection.classify()
        print("Emotions: ", emotions)
        return "happy"
    
    def get_image(self):
        # TODO: Get image from Raspberry Pi
        img = 'groupImage2.jpg'
        return img
    
    def get_pi_data(self):
        # TODO: Get data from Raspberry Pi
        return {"light": 200, "temperature": 20.1}

    def get_data(self): 
        data = {}

        # image   = self.get_image()
        # pi_data = self.get_pi_data()

        # face_count = self.get_face_count(image)

        # self.extract_faces(image)

        # emotions = self.get_emotion()

        face_count = 0 
        emotions = "happy"
        pi_data = {"light": 200, "temperature": 20.1}

        data['count']   = face_count
        data['emotion'] = emotions
        data.update(pi_data)
        return pd.DataFrame([data])


if __name__ == "__main__":
    computer_vision = ComputerVision()

    while(True):
        image = input('Enter image name (or exit to end): ')
        if image == 'exit':
            sys.exit()

        if not os.path.exists(image):
            print("Error: File not found")
            continue

        computer_vision.get_face_count(image)
        computer_vision.extract_faces(image)
        computer_vision.get_emotion()
        print(computer_vision.get_data())
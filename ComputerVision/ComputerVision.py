import FaceCount
import FaceExtraction
import EmotionDetection
import cv2
import sys
import os
import pandas as pd
import socket

class ComputerVision:
    def __init__(self):
        self.face_count = FaceCount.FaceCount()
        self.face_extraction = FaceExtraction.FaceExtraction()
        self.emotion_detection = EmotionDetection.EmotionDetection()
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 500)  # Set the width
        self.cap.set(4, 500)  # Set the height

        # TCP_IP = '172.20.10.7'
        # TCP_PORT = 2222
        # self.BUFFER_SIZE = 8192

        # self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.s.connect((TCP_IP, TCP_PORT))
    
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
        TCP_IP = '172.20.10.7'
        TCP_PORT = 2222
        BUFFER_SIZE = 8192

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))

        s.send('R'.encode())

        with open('received_image.jpg', 'wb') as file:
            while True:
                data = s.recv(BUFFER_SIZE)
                if not data:
                    break
                file.write(data)
        s.close()

        
        img = 'groupImage2.jpg'
        return img
    
    def get_pi_data(self):
        # TODO: Get data from Raspberry Pi
        return {"light": 200, "temperature": 20.1}

    def get_webcam_image(self):
        ret, frame = self.cap.read()
        cv2.imwrite('received_image.jpg', frame)

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
            computer_vision.cap.release()
            sys.exit()

        # if not os.path.exists(image):
        #     print("Error: File not found")
        #     continue

        # computer_vision.get_image()
        computer_vision.get_webcam_image()

        computer_vision.get_face_count('received_image.jpg')
        computer_vision.extract_faces('received_image.jpg')
        computer_vision.get_emotion()
        print(computer_vision.get_data())
    

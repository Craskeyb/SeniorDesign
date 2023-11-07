import FaceCount
import FaceExtraction
import EmotionDetection
import cv2
import sys
import os
import pandas as pd
import socket
import json
class ComputerVision:
    # Contructor
    def __init__(self):
        self.face_count = FaceCount.FaceCount()
        self.face_extraction = FaceExtraction.FaceExtraction()
        self.emotion_detection = EmotionDetection.EmotionDetection()
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 500)  # Set the width
        self.cap.set(4, 500)  # Set the height
    
    def get_face_count(self, image):
        count = self.face_count.get_face_count(image)
        return count
    
    def extract_faces(self, image):
        count = self.face_extraction.extract_faces(image)

        print(count, " faces extracted")

    def get_emotion(self):
        emotions = self.emotion_detection.classify()
        print("Emotions: ", emotions)
        return emotions
    
    # TODO: Refine this and clean up unnecessary code
    def get_image(self):
        # TODO: Get image from Raspberry Pi
        # TCP_IP = '172.20.10.7'
        TCP_IP = '192.168.137.99'

        TCP_PORT = 2222
        BUFFER_SIZE = 8192
        

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        s.connect((TCP_IP, TCP_PORT))
        s.send('R'.encode())
        data = s.recv(BUFFER_SIZE)

        rec_data = json.loads(data.decode('utf-8'))
        rec_data1 = rec_data['Light']
        rec_data2 = rec_data['Temp']
        rec_img = rec_data['image_data']

        with open('rec_img.jpg', 'wb') as f:
            f.write(rec_img)

        s.close()

        # print(rec_data1, rec_data2)

        # s.send('R'.encode())
        # l = s.recv(BUFFER_SIZE)
        # t = s.recv(BUFFER_SIZE)
        # print("t", t, "l", l)
        
        # l = l.decode('utf-8')
        # t = t.decode('utf-8')

        # print("t", t, "l", l)

        # with open('received_image.jpg', 'wb') as file:
        #     while True:
        #         data = s.recv(BUFFER_SIZE)
        #         if not data:
        #             break
        #         file.write(data)
        

        # s.close()
        
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

        # ! Comment/uncomment following to either get image from raspberry pi or from webcam
        # computer_vision.get_image()
        computer_vision.get_webcam_image()

        # Get count of faces
        count = computer_vision.get_face_count('received_image.jpg')

        # Extract faces from image
        computer_vision.extract_faces('received_image.jpg')

        # Get emotions of extracted faces
        emotions = computer_vision.get_emotion()

        # Normalize emotions dict to follow standard
        emotions = computer_vision.norm_emotions(emotions)

        # TODO: Need to get actual data from pi
        pi_data = {"temperature": 20.1, "light": 150}

        data['count']   = count
        data.update(emotions)
        data.update(pi_data)
        return pd.DataFrame([data])
    
    def norm_emotions(self, emotions):
        for emotion in emotions:
            # Change from None to 0
            if emotions[emotion] == None:
                emotions[emotion] = 0
            
        maxEmotion = max(emotions, key= lambda x: emotions[x])
        for emotion in emotions:
            # Logic to set max occurring to 1 and then rest to 0
            if emotion == maxEmotion:
                emotions[emotion] = 1
            else:
                emotions[emotion] = 0

        return emotions

# ! COMMENT THIS OUT IF IMPORTING
if __name__ == "__main__":
    computer_vision = ComputerVision()

    while(True):
        cmd = input('Press enter to process or type \'exit\' to end: ')
        if cmd == 'exit':
            computer_vision.cap.release()
            sys.exit()

        print(computer_vision.get_data())
    

# import FaceCount
from ComputerVision import FaceCount, FaceExtraction, MotionDetection, EmotionDetection
# import FaceExtraction
# import EmotionDetection
# import MotionDetection
import cv2
import sys
import os
import pandas as pd
import socket
import json
import base64
import time

class ComputerVision:
    """
    Constructor to initialize submodules and set config values
    """
    def __init__(self):
        # Initialize all submodules
        self.face_count = FaceCount.FaceCount()
        self.face_extraction = FaceExtraction.FaceExtraction()
        self.emotion_detection = EmotionDetection.EmotionDetection()
        self.motion_detection = MotionDetection.MotionDetection()

        # Configure webcam capture settings (temporary for testing)
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 500)  # Set the width
        self.cap.set(4, 500)  # Set the height
    
    """
    Get face count using FaceCount module

    Returns:
        An int containing the count of faces detected
    """
    def get_face_count(self, image):
        count = self.face_count.get_face_count(image)
        return count
    
    """
    Extract faces using FaceExtraction module
    """
    def extract_faces(self, image):
        count = self.face_extraction.extract_faces(image)

        print(count, " faces extracted")

    """
    Get emotions using EmotionDetection module

    Returns:
        A dict containing each emotion as a key and the number of faces with that emotion as the value
    """
    def get_emotion(self):
        emotions = self.emotion_detection.classify()
        print("Emotions: ", emotions)
        return emotions
    
    
    """
    Connects to a Raspberry Pi and retrieves data including an image, light value, and temperature value.

    Args:
        image_name (str): The name of the image file to be saved.

    Returns:
        Tuple: A tuple containing the light value and temperature value.
    """
    def get_pi_data(self, image_name):
        # Raspberry Pi Socket configuration
        TCP_IP      = '192.168.137.244'
        TCP_PORT    = 2222
        BUFFER_SIZE = 8192
        
        # Establish connection with TCP socket
        print("Attempting to connect to raspberry pi...")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # s.settimeout(3)
        try:
            s.connect((TCP_IP, TCP_PORT))
        except socket.timeout:
            print("Unable to establish connection to raspberry pi, timed out")
            raise RuntimeError
        print("Connected to raspberry pi @\n", TCP_IP)


        # Send 'R' to request data
        inp = 'R'
        s.send(inp.encode('utf-8'))
        data = b''
        print("Requested Data...")

        # Receive until no packets remain
        while True:
            packet = s.recv(BUFFER_SIZE)  # Adjust the buffer size depending on your image size
            if not packet:
                break
            data += packet
        # Attempt to convert received data to values and image
        try:
            received_data = json.loads(data.decode('utf-8'))

            # Extract the values
            light_val = received_data['Light']
            temp_val  = received_data['Temp']

            # Convert the base64 string back to bytes
            received_image_data_base64 = received_data['image_data']
            received_image_data        = base64.b64decode(received_image_data_base64)

            # Write the image data to a file
            with open(image_name, 'wb') as f:
                f.write(received_image_data)

            # Use the received data as needed
            print(f"Light: {light_val}")
            print(f"Temp: {temp_val}")
            print("Image file received.")

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
        except Exception as error:
            print("Error occured while converting data:", error)

        # Close the connection
        s.close()

        return (temp_val, light_val)

    """
    Takes an image using the webcam. Used for testing purposes in place of the raspberry pi
    """
    def get_webcam_image(self):
        ret, frame = self.cap.read()
        cv2.imwrite('ComputerVision\\received_image.jpg', frame)

    """
    Gets motion using MotionDetection module

    Returns:
        TODO: define the type in which motion is returned
    """
    def get_motion(self):
        motion = self.motion_detection.get_motion()
        return motion

    
    """
    Returns a pandas DataFrame containing face count, emotions, and sensor data from raspberry pi

    Returns:
    pandas.DataFrame: A DataFrame containing the data
    """
    def get_data(self): 
        data = {}

        temp1, temp2 = 0, 0
        light1, light2 = 0, 0

        try:
            # Get first image and measurements
            (temp1, light1) = self.get_pi_data('ComputerVision\\received_image.jpg')
            #computer_vision.get_webcam_image()
        except Exception as error:
            print("Error: Error occured while retrieving Raspberry Pi Data")
            print("ERROR:", error)
            raise RuntimeError 
            return

        # Get count of faces
        count = self.get_face_count('ComputerVision\\received_image.jpg')

        # ! This mightExtract faces from image
        # self.extract_faces('ComputerVision\\received_image.jpg')

        # Get emotions of extracted faces
        emotions = self.get_emotion()

        # Normalize emotions dict to follow standard
        emotions = self.norm_emotions(emotions)


        # # Get second image and measurements
        (temp2, light2) = self.get_pi_data('ComputerVision\\received_image1.jpg')  

        # Calculate average of pi sensor data
        temperature = (temp1 + temp2)/2
        light       = (light1 + light2)/2

        # Calculate the motion using the two images received
        # TODO : Uncomment this # motion = computer_vision.get_motion()
        motion = self.get_motion()
        print("Detected Motion:", motion)

        pi_data = {"temperature": temperature, "light": light}

        data['count']   = count
        data.update(emotions)
        data.update(pi_data)
        return (pd.DataFrame([data]), motion)
    
    """
    Normalizes the emotions dictionary by converting any None values to 0, finding the max occurring emotion, 
    and setting its value to 1 while setting all other emotions to 0. If no faces are found, default
    to neutral emotion.

    Args:
        emotions (dict): A dictionary containing the emotions and their corresponding values.

    Returns:
        dict: A dictionary containing the normalized emotions with the max occurring emotion set to 1 and all 
        other emotions set to 0.
    """
    def norm_emotions(self, emotions):
        # Flag for if there is an emotion
        faceFound = False

        # Change from None to 0
        for emotion in emotions:
            if emotions[emotion] == None:
                emotions[emotion] = 0
            else:
                faceFound = True

        # If there is >= 1 face find max occurring, else default to neutral emotion if no faces are found
        if faceFound:   
            maxEmotion = max(emotions, key= lambda x: emotions[x])
        else:
            maxEmotion = 'neutral'

        # Logic to set max occurring to 1 and then rest to 0
        for emotion in emotions:
            if emotion == maxEmotion:
                emotions[emotion] = 1
            else:
                emotions[emotion] = 0

        return emotions


# ! COMMENT THIS OUT IF IMPORTING. Used for testing module without Music Selection Algorithm
# if __name__ == "__main__":
#     computer_vision = ComputerVision()

#     while(True):
#         print('--------------------------------------------------')
#         cmd = input('Press enter to process or type \'exit\' to end: ')
#         if cmd == 'exit':
#             computer_vision.cap.release()
#             sys.exit()

#         print(computer_vision.get_data())
    

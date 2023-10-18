import cv2
import time
import shutil
import os

class FaceExtraction:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.scale_factor = 4
    
    def extract_faces(self, image):
        start = time.time()

        original_img = cv2.imread(image)

        img = cv2.resize(original_img, (int((original_img.shape[1]*(1/self.scale_factor))), int(original_img.shape[0]*(1/self.scale_factor)))) 

        im = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = self.face_cascade.detectMultiScale(im, 1.1, 9)

        self.save_faces(faces, original_img)

        end = time.time()

        print("FaceExtraction Execution Time: ", (end-start), "s")

        return len(faces)

    def save_faces(self, faces, image):
        self.clear_output_folder()

        for i, face in enumerate(faces):
            x1 = face[0]
            y1 = face[1]
            x2 = x1 + face[2]
            y2 = y1 + face[3]

            x1_scaled = x1 * self.scale_factor
            x2_scaled = x2 * self.scale_factor
            y1_scaled = y1 * self.scale_factor
            y2_scaled = y2 * self.scale_factor

            extracted_face = image[y1_scaled:y2_scaled, x1_scaled:x2_scaled]
            extracted_face = cv2.resize(extracted_face, (50,50))

            fname = "faces\\face" + str(i) + ".jpg"

            cv2.imwrite(fname, extracted_face)

    def clear_output_folder(self):
        try:
            shutil.rmtree('faces')
            os.makedirs('faces')
        except Exception as e:
            print("Error: ", e)
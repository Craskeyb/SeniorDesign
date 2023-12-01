import cv2
import time
import face_detection
import shutil
import os
import matplotlib.pyplot as plt

class FaceCount:

    def __init__(self) -> None:
        self.detector = face_detection.build_detector("DSFDDetector", confidence_threshold=0.5, nms_iou_threshold=0.3)
        self.scale_factor = 4
        self.face_cascade = cv2.CascadeClassifier('ComputerVision\\haarcascade_eye.xml')
    
    def get_face_count(self, image):
        start = time.time()
        original_img = cv2.imread(image)

        img = cv2.resize(original_img, (int((original_img.shape[1]*(1/self.scale_factor))), int(original_img.shape[0]*(1/self.scale_factor)))) 

        im = img[:, :, ::-1]

        img_color = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  
        faces = self.detector.detect(im)

        face_image = self.draw_faces(faces, img_color)
        self.save_faces(faces, original_img)

        plt.figure("Detected Faces")
        plt.imshow(face_image, cmap='gray')
        plt.title("Faces Detected: " + str(len(faces)))
        plt.show(block=False)


        end = time.time()

        print("FaceCount Execution time: ", end-start, "s")

        return len(faces)

    def draw_faces(self, faces, image):
        for face in faces:
            if face.item(4) >= 0.1:
                x1 = int(face.item(0))
                y1 = int(face.item(1))
                x2 = int(face.item(2))
                y2 = int(face.item(3))

                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

        return image
    
    def save_faces(self, faces, image):
        self.clear_output_folder()

        for i, face in enumerate(faces):
            x1 = int(face.item(0))
            y1 = int(face.item(1))
            x2 = int(face.item(2))
            y2 = int(face.item(3))

            x1_scaled = x1 * self.scale_factor
            x2_scaled = x2 * self.scale_factor
            y1_scaled = y1 * self.scale_factor
            y2_scaled = y2 * self.scale_factor

            extracted_face = image[y1_scaled:y2_scaled, x1_scaled:x2_scaled]
            # extracted_face = cv2.resize(extracted_face, (100,100))
            extracted_face = cv2.cvtColor(extracted_face, cv2.COLOR_BGR2GRAY)

            fname = "ComputerVision\\faces\\face" + str(i) + ".jpg"

            # self.validate_face(extracted_face, fname)

            cv2.imwrite(fname, extracted_face)

    def clear_output_folder(self):
        try:
            shutil.rmtree('ComputerVision\\faces')
            os.makedirs('ComputerVision\\faces')
        except Exception as e:
            print("Error: ", e)

    def validate_face(self, face_im, name):
        face_im2 = cv2.resize(face_im, (48,48))
        face_im2 = cv2.copyMakeBorder(face_im2,150,150,150,150,cv2.BORDER_CONSTANT)
        faces = self.face_cascade.detectMultiScale(face_im2, 1.1, 5)
        if len(faces):
            plt.imshow(face_im2, cmap='gray')
            plt.show(block=False)
            print("Face Validation")
            print(faces)
            cv2.imwrite(name, face_im)
        
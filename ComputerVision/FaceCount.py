import cv2
import time
import face_detection
import shutil
import os
import matplotlib.pyplot as plt

class FaceCount:
    """
    Constructor to initialize detector models
    """
    def __init__(self) -> None:
        self.detector = face_detection.build_detector("DSFDDetector", confidence_threshold=0.5, nms_iou_threshold=0.3)
        self.scale_factor = 4
        self.face_cascade = cv2.CascadeClassifier('ComputerVision\\haarcascade_eye.xml')
    
    """
    Gets the count of faces from an imput image
    Also optionally does:
        1. Display image with faces highlighted
        2. Save individual faces in image files

    Args:
        image: the image to count faces in
    Returns:
        int: a count of the faces detected
    """
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

    """
    Draws boxes around the detected faces on the original image

    Args:
        faces: list of detected faces
        image: original image to draw box on
    """
    def draw_faces(self, faces, image):
        for face in faces:
            if face.item(4) >= 0.1:
                x1 = int(face.item(0))
                y1 = int(face.item(1))
                x2 = int(face.item(2))
                y2 = int(face.item(3))

                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

        return image
    
    """
    Save the detected faces

    Args:
        faces: list of detected faces
        image: original image to extract face from
    """
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
            extracted_face = cv2.cvtColor(extracted_face, cv2.COLOR_BGR2GRAY)

            fname = "ComputerVision\\faces\\face" + str(i) + ".jpg"

            # Optional call to further validate detected faces before saving
            # self.validate_face(extracted_face, fname)

            # Only use if not validating faces!
            cv2.imwrite(fname, extracted_face)

    """
    Clears the output folder of all previously extracted faces
    """
    def clear_output_folder(self):
        try:
            shutil.rmtree('ComputerVision\\faces')
            os.makedirs('ComputerVision\\faces')
        except Exception as e:
            print("Error: ", e)

    
    """
    Validates a face by checking if eyes are present using cascade detector.
    If >1 eye is detected, save the image

    Args:
        face_im: image to validate
        name: name to save file as
    """
    def validate_face(self, face_im, name):
        face_im2 = cv2.resize(face_im, (48, 48))
        face_im2 = cv2.copyMakeBorder(face_im2, 150, 150, 150, 150, cv2.BORDER_CONSTANT)

        eyes = self.face_cascade.detectMultiScale(face_im2, 1.1, 5)

        if len(eyes):
            cv2.imwrite(name, face_im)
        
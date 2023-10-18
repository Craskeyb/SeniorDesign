import FaceCount
import FaceExtraction
import cv2
import sys
import os

class ComputerVision:
    def __init__(self):
        self.face_count = FaceCount.FaceCount()
        self.face_extraction = FaceExtraction.FaceExtraction()
    
    def get_face_count(self, image):
        im = "groupImage1.jpg"

        count = self.face_count.get_face_count(image)

        print(count, " faces detected")
    
    def extract_faces(self, image):
        im = "groupImage1.jpg"

        count = self.face_extraction.extract_faces(image)

        print(count, " faces extracted")


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

    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cv2.destroyAllWindows()
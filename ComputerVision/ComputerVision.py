import FaceCount
import FaceExtraction
import cv2

class ComputerVision:
    def __init__(self):
        self.face_count = FaceCount.FaceCount()
        self.face_extraction = FaceExtraction.FaceExtraction()
    
    def get_face_count(self):
        im = "groupImage1.jpg"

        count = self.face_count.get_face_count(im)

        print(count, " faces detected")
    
    def extract_faces(self):
        im = "groupImage1.jpg"

        count = self.face_extraction.extract_faces(im)

        print(count, " faces extracted")


if __name__ == "__main__":
    computer_vision = ComputerVision()
    computer_vision.get_face_count()
    computer_vision.extract_faces()

    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cv2.destroyAllWindows()
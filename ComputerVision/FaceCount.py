import cv2
import time
import face_detection

class FaceCount:

    def __init__(self) -> None:
        self.detector = face_detection.build_detector("DSFDDetector", confidence_threshold=0.5, nms_iou_threshold=0.3)
        self.scale_factor = 4
    
    def get_face_count(self, image):
        start = time.time()
        original_img = cv2.imread(image)

        img = cv2.resize(original_img, (int((original_img.shape[1]*(1/self.scale_factor))), int(original_img.shape[0]*(1/self.scale_factor)))) 

        im = img[:, :, ::-1]
  
        faces = self.detector.detect(im)

        face_image = self.draw_faces(faces, img)

        # cv2.imshow("Detected Faces", face_image)

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
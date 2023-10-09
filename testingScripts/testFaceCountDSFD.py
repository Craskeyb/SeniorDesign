# Import required libraries
import cv2
import numpy as np
import dlib
import time

import face_detection

scale_factor = 4
output_scale = 2

detector = face_detection.build_detector("DSFDDetector", confidence_threshold=0.5, nms_iou_threshold=0.3)
start = time.time()

original_img = cv2.imread("groupImage4.jpg")

img = cv2.resize(original_img, (int((original_img.shape[1]*(1/scale_factor))), int(original_img.shape[0]*(1/scale_factor)))) 

im = img[:, :, ::-1]
  
faces = detector.detect(im)
print(faces)

i = 0
for face in faces:
    if face.item(4) >= 0.1:
        x1 = int(face.item(0))
        y1 = int(face.item(1))
        x2 = int(face.item(2))
        y2 = int(face.item(3))

        x1_scaled = x1 * scale_factor
        x2_scaled = x2 * scale_factor
        y1_scaled = y1 * scale_factor
        y2_scaled = y2 * scale_factor

        print(x1, y1, x2, y2)
        roi = original_img[y1_scaled:y2_scaled, x1_scaled:x2_scaled]

        fname = "frame" + str(i) + ".jpg"

        cv2.imshow(fname, roi)
        cv2.imwrite(fname, roi)
        cv2.rectangle(img, (int(face.item(0)), int(face.item(1))), (int(face.item(2)), int(face.item(3))), (0, 255, 0), 2)

        i = i + 1

cv2.imshow('frame', img)

end = time.time()

print("Execution Time :", (end-start), "s")
print("Faces Detected: ", len(faces))

while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
cv2.destroyAllWindows()

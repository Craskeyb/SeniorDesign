import cv2
import time
import dlib
import mtcnn


scale_factor = 4
detector = mtcnn.MTCNN()

start = time.time()
original_img = cv2.imread("groupImage1.jpg")

img = cv2.resize(original_img, (int((original_img.shape[1]*(1/scale_factor))), int(original_img.shape[0]*(1/scale_factor)))) 

im = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  

faces = detector.detect_faces(im)
print(faces)

i = 0
for face in faces:
    x1 = face['box'][0]
    y1 = face['box'][1]
    x2 = x1 + face['box'][2]
    y2 = y1 + face['box'][3]

    x1_scaled = x1 * scale_factor
    x2_scaled = x2 * scale_factor
    y1_scaled = y1 * scale_factor
    y2_scaled = y2 * scale_factor

    print(x1, y1, x2, y2)
    roi = original_img[y1_scaled:y2_scaled, x1_scaled:x2_scaled]

    fname = "output\frame" + str(i) + ".jpg"

    cv2.imshow(fname, roi)
    cv2.imwrite(fname, roi)
    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

    i = i + 1

cv2.imshow('frame', img)

end = time.time()

print("Execution Time :", (end-start), "s")
print("Faces Detected: ", len(faces))

while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
cv2.destroyAllWindows()

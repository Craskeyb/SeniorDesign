# Import required libraries
import cv2
import numpy as np
import dlib
import time
import csv

import face_detection

scale_factor = 2

detector = face_detection.build_detector("DSFDDetector", confidence_threshold=0.5, nms_iou_threshold=0.3)

with open('testingDatas\\train\\train.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

out = []

for i in range(1,len(data)):
    file = data[i]
    f_name = 'testingDatas\\train\\image_data\\' + file[0]

    print(f_name)

    original_img = cv2.imread(f_name)

    img = cv2.resize(original_img, (int((original_img.shape[1]*(1/scale_factor))), int(original_img.shape[0]*(1/scale_factor)))) 

    im = img[:, :, ::-1]
    
    faces = detector.detect(im)

    print(len(faces))

    out.append([file[0], len(faces)])



np.savetxt("dsfd_output.csv",
           out,
           delimiter = ", ",
           fmt = '% s')


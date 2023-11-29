import cv2
import numpy as np
import matplotlib.pyplot as plt

class MotionDetection:
    def __init__(self):
        pass


    def get_motion(self):
        val = 100 
        
        im1 = cv2.imread("ComputerVision\\received_image.jpg")
        im1 = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
        im1 = cv2.resize(im1, [500,500])
        im1_blur = cv2.GaussianBlur(im1, [21,21], 2)

        im2 = cv2.imread("ComputerVision\\received_image1.jpg")
        im2 = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)
        im2 = cv2.resize(im2, [500,500])
        im2_blur = cv2.GaussianBlur(im2, [21,21], 2)

        diff = cv2.absdiff(src1=im1_blur, src2 = im2_blur)
        diff = cv2.threshold(src=diff, thresh=50, maxval=255, type=cv2.THRESH_BINARY)[1]

        whitePixels = np.sum(diff == 255)
        motion = whitePixels / (500*500)

        if(motion > 0.25):
            motionVal = 'High'
        elif(motion < 0.05):
            motionVal = 'Low'
        else:
            motionVal = 'Medium'
        
        plt.figure("Motion Detection")
        plt.subplot(1,3,1)
        plt.imshow(im1, cmap='gray')
        plt.subplot(1,3,2)
        plt.imshow(im2, cmap='gray')
        plt.subplot(1,3,3)
        plt.imshow(diff, cmap='gray')
        plt.tight_layout()
        plt.suptitle("Detected Motion:" + motionVal)
        plt.show(block=False)
        
        return motionVal
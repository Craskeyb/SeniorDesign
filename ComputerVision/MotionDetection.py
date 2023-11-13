import cv2
import numpy as np

class MotionDetection:
    def __init__(self):
        print("Motion Detection init")


    def get_motion(self):
        val = 100 

        im1 = cv2.imread("ComputerVision\\received_image.jpg")
        im1 = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
        im1 = cv2.resize(im1, [500,500])
        im1 = cv2.GaussianBlur(im1, [21,21], 2)
        cv2.imshow('im1', im1)

        im2 = cv2.imread("ComputerVision\\received_image1.jpg")
        im2 = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)
        im2 = cv2.resize(im2, [500,500])
        im2 = cv2.GaussianBlur(im2, [21,21], 2)
        cv2.imshow('im2', im2)
        cv2.waitKey(0)

        diff = cv2.absdiff(src1=im1, src2 = im2)
        diff = cv2.threshold(src=diff, thresh=50, maxval=255, type=cv2.THRESH_BINARY)[1]
        cv2.imshow('diff', diff)

        whitePixels = np.sum(diff == 255)
        motion = whitePixels / (500*500)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        if(motion > 0.25):
            return 'High'
        elif(motion < 0.05):
            return 'Low'
        else:
            return 'Medium'
        

# if __name__ == "__main__":
#     motion_detection = MotionDetection()
#     print(motion_detection.get_motion())



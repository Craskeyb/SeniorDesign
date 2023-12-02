import cv2
import numpy as np
import matplotlib.pyplot as plt

class MotionDetection:
    def __init__(self):
        pass


    """
    Calculates the level of motion detected between two images

    Returns:
        str: The level of motion detected, 'High', 'Medium', or 'Low'.
    """
    def get_motion(self):
        
        # Read in first image, convert to gray, resize, and apply Gaussian Blur
        im1 = cv2.imread("ComputerVision\\received_image.jpg")
        im1 = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
        im1 = cv2.resize(im1, [500,500])
        im1_blur = cv2.GaussianBlur(im1, [21,21], 2)

        # Read in second image, convert to gray, resize, and apply Gaussian Blue
        im2 = cv2.imread("ComputerVision\\received_image1.jpg")
        im2 = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)
        im2 = cv2.resize(im2, [500,500])
        im2_blur = cv2.GaussianBlur(im2, [21,21], 2)

        # Subtract pixel values between images to get difference
        diff = cv2.absdiff(src1=im1_blur, src2 = im2_blur)

        # Threshold values from difference image such that <50 goes to 0 and >50 goes to 255
        diff = cv2.threshold(src=diff, thresh=50, maxval=255, type=cv2.THRESH_BINARY)[1]

        # Count the number of pixels over the threshold difference
        whitePixels = np.sum(diff == 255)

        # Calculate the percentage of pixels that were over the threshold difference
        motion = whitePixels / (500*500)

        # Classify as High, Medium, or Low based on paramters
        if(motion > 0.25):
            motionVal = 'High'
        elif(motion < 0.05):
            motionVal = 'Low'
        else:
            motionVal = 'Medium'
        
        # Plot the imput images, and the difference image to visualize the motion computation
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
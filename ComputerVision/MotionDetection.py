import cv2

class MotionDetection:
    def __init__(self):
        print("Motion Detection init")

    def get_motion(self):
        im1 = cv2.imread("received_image.jpg")
        im1 = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
        im2 = cv2.imread("received_image1.jpg")
        im2 = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)



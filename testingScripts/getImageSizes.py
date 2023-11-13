import cv2

for i in range(1, 8):
  image_name = "groupImage" + str(i) + ".jpg"
  image = cv2.imread(image_name)
  dimensions = image.shape
  print(dimensions)
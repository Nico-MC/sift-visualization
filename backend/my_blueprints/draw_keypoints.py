# import cv2
# import numpy as np
#
# img = cv2.imread('home.jpg')
# gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# sift = cv2.xfeatures2d.SIFT_create()
# kp = sift.detect(gray,None)
# img=cv2.drawKeypoints(gray,kp,img)
# cv2.imwrite('sift_keypoints.jpg',img)

import cv2, numpy as np

def draw_keypoints(inputImage_name):
    img = cv2.imread(inputImage_name)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    sift = cv2.xfeatures2d.SIFT_create()
    kp = sift.detect(gray,None)
    for point in kp:
        print(point.pt)

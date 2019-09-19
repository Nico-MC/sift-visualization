from flask import jsonify
import cv2 as cv, numpy as np

def handle_keypoints(features_string, inputImage_path):
    img = cv.imread(inputImage_path)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    sift = cv.xfeatures2d.SIFT_create()
    kp = sift.detect(gray, None)

    img = cv.drawKeypoints(gray, kp, img, flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv.imwrite("./static/keypoints/keypoints_openCV.jpg", img)

    features = features_string.splitlines()
    return jsonify(features)

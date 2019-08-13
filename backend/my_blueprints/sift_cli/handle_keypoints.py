from flask import jsonify
import cv2 as cv, numpy as np

def handle_keypoints(features_string, inputImage_path):
    features = features_string.splitlines()
    keypoints = []
    for feature in features:
        y = feature.split(' ')[0]
        x = feature.split(' ')[1]
        sigma = feature.split(' ')[2]
        theta = feature.split(' ')[3]
        octa = feature.split(' ')[4]
        sca = feature.split(' ')[5]
        keypoints.append(cv.KeyPoint(x = float(x), y = float(y)
            , _size = float(sigma) * 2
            , _angle = np.degrees(float(theta))
            , _response = 0
            , _octave = 0
            , _class_id = -1))
    draw_keypoints(keypoints, inputImage_path)

    return jsonify(features)

def draw_keypoints(keypoints, inputImage_path):
    img = cv.imread(inputImage_path)
    img2 = cv.imread(inputImage_path)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray2 = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    sift = cv.xfeatures2d.SIFT_create()
    kp = sift.detect(gray, None)

    img = cv.drawKeypoints(gray, keypoints, img, flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv.imwrite("./static/keypoints/" + inputImage_path.split("/")[-1].split(".png")[0] + ".jpg", img)

    img2 = cv.drawKeypoints(gray2, kp, img2, flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv.imwrite("./static/keypoints/" + inputImage_path.split("/")[-1].split(".png")[0] + "_cv.jpg", img2)

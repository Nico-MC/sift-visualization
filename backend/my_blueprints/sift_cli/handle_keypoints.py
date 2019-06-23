from flask import jsonify
import cv2 as cv, numpy as np

def handle_keypoints(features_string, inputImage_path):
    features = features_string.splitlines()
    keypoints = []
    for feature in features:
        x = feature.split(' ')[1]
        y = feature.split(' ')[0]
        sigma = feature.split(' ')[2]
        theta = feature.split(' ')[3]
        octa = feature.split(' ')[4]
        sca = feature.split(' ')[5]
        keypoints.append(cv.KeyPoint(x = float(x), y = float(y)
            , _size = 0
            , _angle = 0
            , _response = 0
            , _octave = 0
            , _class_id = 0))
    draw_keypoints(keypoints, inputImage_path)

    return jsonify(features)

def draw_keypoints(keypoints, inputImage_path):
    img = cv.imread(inputImage_path)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    img = cv.drawKeypoints(gray, keypoints, img)
    cv.imwrite("./static/keypoints/" + inputImage_path.split("/")[-1].split(".png")[0] + ".png", img)

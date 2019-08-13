from flask import request, Blueprint, current_app as app, jsonify
import cv2 as cv, numpy as np, uuid

animate_keypoints = Blueprint('animate_keypoints', __name__)

@animate_keypoints.route('/animate_keypoints', methods=['GET'])
def sift_cli_animate_keypoints():
    inputImageName = request.args.get('inputImageName')
    inputImagePath = app.config["ASSETS_FOLDER"] + '/' + inputImageName
    label = "_1"
    allKeypoints = {
        "0": get_keypoints("extra_NES", label, inputImageName),
        "1": get_keypoints("extra_DoGSoftThresh", label, inputImageName),
        "2": get_keypoints("extra_ExtrInterp", label, inputImageName),
        "3": get_keypoints("extra_DoGThresh", label, inputImageName),
        "4": get_keypoints("extra_OnEdgeResp", label, inputImageName),
        "5": get_keypoints("extra_FarFromBorder", label, inputImageName),
        "randomUuid": uuid.uuid4()
    }

    img = cv.imread(inputImagePath + ".png")
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    cv.imwrite( "static/keypoints/" + inputImageName + "_gray.jpg", gray);

    return jsonify(allKeypoints)

def get_keypoints(filename, label, inputImageName):
    file = open("static/keypoints/" + filename + label + ".txt", "r")
    keypointsFromFile = file.read()
    keypointsFromFile = keypointsFromFile.splitlines()
    keypoints = []
    for line in keypointsFromFile:
        y = line.split(' ')[0]
        x = line.split(' ')[1]
        sigma = line.split(' ')[2]
        theta = line.split(' ')[3]
        octa = line.split(' ')[4]
        sca = line.split(' ')[5]
        keypoints.append({
            "x": float(x),
            "y": float(y),
            "_size": float(sigma) * 62,
            "_angle": np.degrees(float(theta)),
            "_response": 0,
            "_octave": 0,
            "_class_id": -1})

    return keypoints

    # img = cv.drawKeypoints(gray, keypoints, img)
    # cv.imwrite("./static/keypoints/" + inputImageName + "_" + filename + ".jpg", img)

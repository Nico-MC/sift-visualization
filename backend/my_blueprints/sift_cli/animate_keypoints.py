from flask import request, Blueprint, current_app as app, jsonify
import cv2 as cv, numpy as np, uuid, os, shutil

animate_keypoints = Blueprint('animate_keypoints', __name__)

@animate_keypoints.route('/animate_keypoints', methods=['GET'])
def sift_cli_animate_keypoints():
    inputImageName = request.args.get('inputImageName')
    inputImagePath = app.config["ASSETS_FOLDER"] + '/' + inputImageName
    label = "_1"
    img = cv.imread(inputImagePath + ".png")
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    cv.imwrite( "static/keypoints/" + inputImageName + "_gray.jpg", gray);

    allKeypoints = {
        "0": get_keypoints("extra_NES", label, inputImageName, "step_1", img, gray),
        "1": get_keypoints("extra_DoGSoftThresh", label, inputImageName, "step_2", img, gray),
        "2": get_keypoints("extra_ExtrInterp", label, inputImageName, "step_3", img, gray),
        "3": get_keypoints("extra_DoGThresh", label, inputImageName, "step_4", img, gray),
        "4": get_keypoints("extra_OnEdgeResp", label, inputImageName, "step_5", img, gray),
        "5": get_keypoints("extra_FarFromBorder", label, inputImageName, "step_6", img, gray),
        "randomUuid": uuid.uuid4()
    }

    return jsonify(allKeypoints)

def get_keypoints(filename, label, inputImageName, step, img, gray):
    currentDirectoryPath = "static/keypoints/" + step + "_" + filename
    check_output_directory(currentDirectoryPath)
    file = open("static/keypoints/" + filename + label + ".txt", "r")
    keypointsFromFile = file.read()
    keypointsFromFile = keypointsFromFile.splitlines()
    justForTesting = {}
    producedKeypointsInThisStep = []
    keypoints = {}
    for line in keypointsFromFile:
        y = line.split(' ')[0]
        x = line.split(' ')[1]
        sigma = line.split(' ')[2]
        theta = line.split(' ')[3]
        octa = line.split(' ')[4]
        sca = line.split(' ')[5]
        justForTesting_kp = ({
                                "x": float(x),
                                "y": float(y),
                                "_size": float(sigma) * 62,
                                "_angle": np.degrees(float(theta)),
                                "_response": 0,
                                "_octave": int(octa),
                                "_class_id": -1
                             })
        keypoint = cv.KeyPoint(
                                x = float(x),
                                y = float(y),
                                _size = float(sigma) * 62,
                                _angle = np.degrees(float(theta)),
                                _response = 0,
                                _octave = int(octa),
                                _class_id = -1
                              )
        producedKeypointsInThisStep.append(keypoint)

        if octa in keypoints.keys():
            if sca in keypoints[octa].keys():
                keypoints[octa][sca].append(keypoint)
                justForTesting[octa][sca].append(justForTesting_kp)
            else:
                keypoints[octa].update({ sca: [keypoint] })
                justForTesting[octa].update({ sca: [justForTesting_kp] })

        else:
            keypoints[octa] = { sca: [keypoint] }
            justForTesting[octa] = { sca: [justForTesting_kp] }
            os.makedirs(currentDirectoryPath + "/Octave_" + octa)

    drawKeypoints(keypoints, currentDirectoryPath, img, gray)

    # Now draw all keypoints of this step to an image
    path = currentDirectoryPath + "/keypoints.jpg"
    img = cv.drawKeypoints(gray, producedKeypointsInThisStep, img)
    cv.imwrite(path, img)

    return justForTesting




def drawKeypoints(keypoints, currentDirectoryPath, img, gray):
    for octave_number, octave in keypoints.items():
        for scale_number, scale in octave.items():
            path = currentDirectoryPath + "/Octave_" + octave_number + "/scale_" + scale_number + ".jpg"
            img = cv.drawKeypoints(gray, scale, img)
            cv.imwrite(path, img)





def check_output_directory(currentDirectoryPath):
    try:
        shutil.rmtree(currentDirectoryPath, ignore_errors = True, onerror = None)
        os.makedirs(currentDirectoryPath)
    except Exception as e:
        return(e)

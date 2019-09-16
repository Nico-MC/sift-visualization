from flask import request, Blueprint, current_app as app, jsonify
import cv2 as cv, numpy as np, uuid, os, shutil, glob, re
from ..lib_demo_sift import *

animate_keypoints = Blueprint('animate_keypoints', __name__)

@animate_keypoints.route('/animate_keypoints', methods=['GET'])
def sift_cli_animate_keypoints():
    inputImageName = request.args.get('inputImageName')
    inputImagePath = app.config["ASSETS_FOLDER"] + '/' + inputImageName
    label = "_1"
    inputImagePath += ".png"
    gray = cv.cvtColor(cv.imread(inputImagePath), cv.COLOR_BGR2GRAY)
    grayImagePath = "static/keypoints/" + inputImageName + "_gray.jpg"
    cv.imwrite(grayImagePath, gray);

    allKeypoints = {
        "0": get_keypoints("extra_NES", label, inputImageName, "step_0", inputImagePath, grayImagePath),
        "1": get_keypoints("extra_DoGSoftThresh", label, inputImageName, "step_1", inputImagePath, grayImagePath),
        "2": get_keypoints("extra_ExtrInterp", label, inputImageName, "step_2", inputImagePath, grayImagePath),
        "3": get_keypoints("extra_DoGThresh", label, inputImageName, "step_3", inputImagePath, grayImagePath),
        "4": get_keypoints("extra_OnEdgeResp", label, inputImageName, "step_4", inputImagePath, grayImagePath),
        "5": get_keypoints("extra_FarFromBorder", label, inputImageName, "step_5", inputImagePath, grayImagePath),
        "randomUuid": uuid.uuid4()
    }

    return jsonify(allKeypoints)

def get_keypoints(filename, label, inputImageName, step, inputImagePath, grayImagePath):
    currentDirectoryPath = "static/keypoints/" + step + "_" + filename
    check_output_directory(currentDirectoryPath)
    filePath = "static/keypoints/" + filename + label + ".txt"
    file = open(filePath, "r")
    keypointsFromFile = file.read()
    keypointsFromFile = keypointsFromFile.splitlines()
    keypoints = {}
    keypoints_scaled = {}
    for line in keypointsFromFile:
        y = line.split(' ')[0]
        x = line.split(' ')[1]
        sigma = line.split(' ')[2]
        theta = line.split(' ')[3]
        octa = line.split(' ')[4]
        sca = line.split(' ')[5]
        keypoint = str(float(y)) + " " + str(float(x)) + " " + str(float(sigma)) + " " + str(np.degrees(float(theta)))
        keypoint_scaled = ({
                                "x": float(x) * 2,
                                "y": float(y) * 2,
                                "_size": float(sigma) / 2,
                                "_angle": np.degrees(float(theta)),
                                "_response": 0,
                                "_octave": int(octa),
                                "_class_id": -1
                    })

        # Sort the keypoint after each octave and each scale
        if octa in keypoints.keys():
            if sca in keypoints[octa].keys():
                keypoints_scaled[octa][sca].append(keypoint_scaled)
                keypoints[octa][sca].append(keypoint)
            else:
                keypoints_scaled[octa].update({ sca: [keypoint_scaled] })
                keypoints[octa].update({ sca: [keypoint] })

        else:
            keypoints_scaled[octa] = { sca: [keypoint_scaled] }
            keypoints[octa] = { sca: [keypoint] }
            os.makedirs(currentDirectoryPath + "/Octave_" + octa + "/Scalespace")
            os.makedirs(currentDirectoryPath + "/Octave_" + octa + "/DoG")

    drawKeypoints(keypoints, currentDirectoryPath, inputImagePath, grayImagePath, step, keypoints_scaled)

    # Now draw all keypoints of this step to an image
    outputImagePath = currentDirectoryPath + "/keypoints.jpg"
    # draw_keys_oriented(filePath, inputImagePath, outputImagePath)

    return keypoints

def drawKeypoints(keypoints, currentDirectoryPath, inputImagePath, grayImagePath, step, keypoints_scaled):
    for octave_number, octave in keypoints.items():
        for scale_number, kp in octave.items():
            path_scaleImageKeypoints = currentDirectoryPath + "/Octave_" + octave_number + "/Scalespace/scale_" + scale_number + ".jpg"
            draw_keys_oriented(kp, grayImagePath, path_scaleImageKeypoints)

    for octave_number, octave in keypoints_scaled.items():
        for scale_number, kp in octave.items():
            path_dogImage = glob.glob("static/dog/*o*" + octave_number + "_s*" + scale_number + ".png")[0]
            path_dogImageKeypoints = currentDirectoryPath + "/Octave_" + octave_number + "/DoG/scale_" + scale_number + ".jpg"
            # draw_keys_oriented(kp, path_dogImage, path_dogImageKeypoints)




def check_output_directory(currentDirectoryPath):
    try:
        shutil.rmtree(currentDirectoryPath, ignore_errors = True, onerror = None)
        os.makedirs(currentDirectoryPath)
    except Exception as e:
        return(e)

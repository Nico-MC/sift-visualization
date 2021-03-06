from flask import request, Blueprint, current_app as app, jsonify
import cv2 as cv, numpy as np, uuid, os, shutil, glob, re
from ..lib_demo_sift import *

animate_keypoints = Blueprint('animate_keypoints', __name__)

@animate_keypoints.route('/animate_keypoints', methods=['GET'])
def sift_cli_animate_keypoints():
    inputImageName = request.args.get('inputImageName')
    drawType = request.args.get('drawType')
    inputImagePath = app.config["ASSETS_FOLDER"] + '/' + inputImageName
    label = "_1"
    inputImagePath += ".png"
    img = cv.imread(inputImagePath)
    gray = cv.cvtColor(cv.imread(inputImagePath), cv.COLOR_BGR2GRAY)
    grayImagePath = "static/keypoints/" + inputImageName + "_gray.jpg"
    cv.imwrite(grayImagePath, gray);

    allKeypoints = {
        "0": get_keypoints("extra_NES", label, inputImageName, "step_0", inputImagePath, grayImagePath, drawType, img, gray),
        "1": get_keypoints("extra_DoGSoftThresh", label, inputImageName, "step_1", inputImagePath, grayImagePath, drawType, img, gray),
        "2": get_keypoints("extra_ExtrInterp", label, inputImageName, "step_2", inputImagePath, grayImagePath, drawType, img, gray),
        "3": get_keypoints("extra_DoGThresh", label, inputImageName, "step_3", inputImagePath, grayImagePath, drawType, img, gray),
        "4": get_keypoints("extra_OnEdgeResp", label, inputImageName, "step_4", inputImagePath, grayImagePath, drawType, img, gray),
        "5": get_keypoints("extra_FarFromBorder", label, inputImageName, "step_5", inputImagePath, grayImagePath, drawType, img, gray),
        "randomUuid": uuid.uuid4()
    }
    return jsonify(allKeypoints)

def get_keypoints(stepname, label, inputImageName, step, inputImagePath, grayImagePath, drawType, img, gray):
    currentDirectoryPath = "static/keypoints/" + step
    check_output_directory(currentDirectoryPath)
    filePath = "static/keypoints/" + stepname + label + ".txt"
    if((drawType == "false") and (step == "step_5")):
        filePath = "static/keypoints/features.txt"
    file = open(filePath, "r")
    keypointsFromFile = file.read()
    keypointsFromFile = keypointsFromFile.splitlines()
    keypoints = {}
    keypoints_scaled = {}
    keypoints_cv = {}
    keypoints_cv_scaled = {}
    allKeypointsInCurrentStep = []
    for line in keypointsFromFile:
        y = line.split(' ')[0]
        x = line.split(' ')[1]
        sigma = line.split(' ')[2]
        theta = line.split(' ')[3]
        octa = line.split(' ')[4]
        sca = line.split(' ')[5]
        if(step == "step_5"):
            keypoint = str(float(y)) + " " + str(float(x)) + " " + str(float(sigma)) + " " + str(float(theta))
            keypoint_scaled = str(float(y) * 2) + " " + str(float(x) * 2) + " " + str(float(sigma) * 2) + " " + str(float(theta))
        else:
            keypoint = str(float(y)) + " " + str(float(x)) + " " + str(float(sigma))
            keypoint_scaled = str(float(y) * 2) + " " + str(float(x) * 2) + " " + str(float(sigma) * 2)
        theta = float(float(theta)*(360/np.pi))
        keypoint_cv = cv.KeyPoint(
                                x = float(x),
                                y = float(y),
                                _size = float(sigma) * 2,
                                _angle = theta,
                                _response = 0,
                                _octave = int(octa),
                                _class_id = -1
                                )
        keypoint_cv_scaled = cv.KeyPoint(
                                x = float(x) * 2,
                                y = float(y) * 2,
                                _size = float(sigma) * 4,
                                _angle = np.radians(theta),
                                _response = 0,
                                _octave = int(octa),
                                _class_id = -1
                                )

        allKeypointsInCurrentStep.append(keypoint)

        # Sort the keypoint after each octave and each scale
        if octa in keypoints.keys():
            if sca in keypoints[octa].keys():
                keypoints_scaled[octa][sca].append(keypoint_scaled)
                keypoints[octa][sca].append(keypoint)
                keypoints_cv_scaled[octa][sca].append(keypoint_cv_scaled)
                keypoints_cv[octa][sca].append(keypoint_cv)
            else:
                keypoints_scaled[octa].update({ sca: [keypoint_scaled] })
                keypoints[octa].update({ sca: [keypoint] })
                keypoints_cv_scaled[octa].update({ sca: [keypoint_cv_scaled] })
                keypoints_cv[octa].update({ sca: [keypoint_cv] })

        else:
            keypoints_scaled[octa] = { sca: [keypoint_scaled] }
            keypoints[octa] = { sca: [keypoint] }
            keypoints_cv_scaled[octa] = { sca: [keypoint_cv_scaled] }
            keypoints_cv[octa] = { sca: [keypoint_cv] }

            os.makedirs(currentDirectoryPath + "/Octave_" + octa + "/Scalespace")
            os.makedirs(currentDirectoryPath + "/Octave_" + octa + "/DoG")
            os.makedirs(currentDirectoryPath + "/Octave_" + octa + "/Original")



    if(drawType == "true"):
        drawKeypoints(keypoints, keypoints_scaled, currentDirectoryPath, inputImagePath, grayImagePath, step, allKeypointsInCurrentStep)
    else:
        drawKeypointsWithCv(keypoints_cv, keypoints_cv_scaled, currentDirectoryPath, inputImagePath, grayImagePath, step, img, gray, allKeypointsInCurrentStep)

    return keypoints

# IPOL
def drawKeypoints(keypoints, keypoints_scaled, currentDirectoryPath, inputImagePath, grayImagePath, step, allKeypointsInCurrentStep):
    draw_keys(allKeypointsInCurrentStep, grayImagePath, currentDirectoryPath + "/keypoints.jpg")
    for octave_number, octave in keypoints.items():
        for scale_number, kp in octave.items():
            path_scaleImageKeypoints = currentDirectoryPath + "/Octave_" + octave_number + "/Original/scale_" + scale_number + ".jpg"
            if(step == "step_5"):
                draw_keys_oriented(kp, grayImagePath, path_scaleImageKeypoints)
            else:
                draw_keys(kp, grayImagePath, path_scaleImageKeypoints)


    for octave_number, octave in keypoints_scaled.items():
        for scale_number, kp in octave.items():
            path_dogImage = glob.glob("static/dog/*o*" + octave_number + "_s*" + scale_number + ".png")[0]
            path_dogImageKeypoints = currentDirectoryPath + "/Octave_" + octave_number + "/DoG/scale_" + scale_number + ".jpg"
            path_scalespaceImage = glob.glob("static/scalespace/*o*" + octave_number + "_s*" + scale_number + ".png")[0]
            path_scalespaceImageKeypoints = currentDirectoryPath + "/Octave_" + octave_number + "/Scalespace/scale_" + scale_number + ".jpg"
            if(step == "step_5"):
                draw_keys_oriented(kp, path_dogImage, path_dogImageKeypoints)
                draw_keys_oriented(kp, path_scalespaceImage, path_scalespaceImageKeypoints)
            else:
                draw_keys(kp, path_dogImage, path_dogImageKeypoints)
                draw_keys(kp, path_scalespaceImage, path_scalespaceImageKeypoints)

# OpenCV
def drawKeypointsWithCv(keypoints_cv, keypoints_cv_scaled, currentDirectoryPath, inputImagePath, grayImagePath, step, img, gray, allKeypointsInCurrentStep):
    for octave_number, octave in keypoints_cv.items():
        for scale_number, kp in octave.items():
            path_scaleImageKeypoints = currentDirectoryPath + "/Octave_" + octave_number + "/Original/scale_" + scale_number + ".jpg"
            img = cv.drawKeypoints(gray, kp, img, flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
            cv.imwrite(path_scaleImageKeypoints, img)

    for octave_number, octave in keypoints_cv_scaled.items():
        for scale_number, kp in octave.items():
            path_dogImage = glob.glob("static/dog/*o*" + octave_number + "_s*" + scale_number + ".png")[0]
            path_dogImageKeypoints = currentDirectoryPath + "/Octave_" + octave_number + "/DoG/scale_" + scale_number + ".jpg"
            path_scalespaceImage = glob.glob("static/scalespace/*o*" + octave_number + "_s*" + scale_number + ".png")[0]
            path_scalespaceImageKeypoints = currentDirectoryPath + "/Octave_" + octave_number + "/Scalespace/scale_" + scale_number + ".jpg"
            dog = cv.imread(path_dogImage)
            ss = cv.imread(path_scalespaceImage)
            # Draw keypoints on DoG image
            dog_kp = cv.drawKeypoints(dog, kp, img, flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
            cv.imwrite(path_dogImageKeypoints, dog_kp)
            # Draw keypoints on SS image
            ss_kp = cv.drawKeypoints(ss, kp, img, flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
            cv.imwrite(path_scalespaceImageKeypoints, ss_kp)


def check_output_directory(currentDirectoryPath):
    try:
        shutil.rmtree(currentDirectoryPath, ignore_errors = True, onerror = None)
        os.makedirs(currentDirectoryPath)
    except Exception as e:
        print(e)

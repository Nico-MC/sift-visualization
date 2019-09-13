from flask import request, Blueprint, current_app as app, jsonify
import cv2 as cv, numpy as np, uuid, os, shutil, glob, re

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
        "0": get_keypoints("extra_NES", label, inputImageName, "step_0", img, gray),
        "1": get_keypoints("extra_DoGSoftThresh", label, inputImageName, "step_1", img, gray),
        "2": get_keypoints("extra_ExtrInterp", label, inputImageName, "step_2", img, gray),
        "3": get_keypoints("extra_DoGThresh", label, inputImageName, "step_3", img, gray),
        "4": get_keypoints("extra_OnEdgeResp", label, inputImageName, "step_4", img, gray),
        "5": get_keypoints("extra_FarFromBorder", label, inputImageName, "step_5", img, gray),
        "randomUuid": uuid.uuid4()
    }

    return jsonify(allKeypoints)

def get_keypoints(filename, label, inputImageName, step, img, gray):
    currentDirectoryPath = "static/keypoints/" + step + "_" + filename
    check_output_directory(currentDirectoryPath)
    file = open("static/keypoints/" + filename + label + ".txt", "r")
    keypointsFromFile = file.read()
    keypointsFromFile = keypointsFromFile.splitlines()
    keypoints_cv_scaled = {}
    keypoints_cv = {}
    keypoints_cv_draw_step = []
    keypoints = {}
    for line in keypointsFromFile:
        y = line.split(' ')[0]
        x = line.split(' ')[1]
        sigma = line.split(' ')[2]
        theta = line.split(' ')[3]
        octa = line.split(' ')[4]
        sca = line.split(' ')[5]
        keypoint = ({
                                "x": float(x),
                                "y": float(y),
                                "_size": float(sigma) * 2,
                                "_angle": np.degrees(float(theta)),
                                "_response": 0,
                                "_octave": int(octa),
                                "_class_id": -1
                    })
        keypoint_cv = cv.KeyPoint(
                                x = float(x),
                                y = float(y),
                                _size = float(sigma) * 2,
                                _angle = np.degrees(float(theta)),
                                _response = 0,
                                _octave = int(octa),
                                _class_id = -1
                                )
        keypoint_cv_scaled = cv.KeyPoint(
                                x = float(x)*2,
                                y = float(y)*2,
                                _size = float(sigma),
                                _angle = np.degrees(float(theta)),
                                _response = 0,
                                _octave = int(octa),
                                _class_id = -1
                                )
        keypoints_cv_draw_step.append(keypoint_cv)

        # Sort the keypoint_cv after each octave and each scale
        if octa in keypoints.keys():
            if sca in keypoints[octa].keys():
                keypoints_cv_scaled[octa][sca].append(keypoint_cv_scaled)
                keypoints_cv[octa][sca].append(keypoint_cv)
                keypoints[octa][sca].append(keypoint)
            else:
                keypoints_cv_scaled[octa].update({ sca: [keypoint_cv_scaled] })
                keypoints_cv[octa].update({ sca: [keypoint_cv] })
                keypoints[octa].update({ sca: [keypoint] })

        else:
            keypoints_cv_scaled[octa] = { sca: [keypoint_cv_scaled] }
            keypoints_cv[octa] = { sca: [keypoint_cv] }
            keypoints[octa] = { sca: [keypoint] }
            os.makedirs(currentDirectoryPath + "/Octave_" + octa)

    drawKeypoints(keypoints_cv, currentDirectoryPath, img, gray, step, keypoints_cv_scaled)

    # Now draw all keypoints of this step to an image
    path = currentDirectoryPath + "/keypoints.jpg"
    img = cv.drawKeypoints(gray, keypoints_cv_draw_step, img)
    cv.imwrite(path, img)

    return keypoints

def drawKeypoints(keypoints_cv, currentDirectoryPath, img, gray, step, keypoints_cv_scaled):
    for octave_number, octave in keypoints_cv.items():
        for scale_number, scale in octave.items():
            path_originalImage = currentDirectoryPath + "/Octave_" + octave_number + "/scale_" + scale_number + ".jpg"
            img = cv.drawKeypoints(gray, scale, img)
            cv.imwrite(path_originalImage, img)

    if(step == "step_5"):
        for octave_number, octave in keypoints_cv_scaled.items():
            for scale_number, scale in octave.items():
                path_scaledImage = "static/scalespace/scalespace_o" + octave_number + "_s" + scale_number + ".jpg"
                file = cv.imread(glob.glob("static/scalespace/*o*" + octave_number + "_s*" + scale_number + ".png")[0])
                img = cv.drawKeypoints(file, scale, file)
                cv.imwrite(path_scaledImage, img)




def check_output_directory(currentDirectoryPath):
    try:
        shutil.rmtree(currentDirectoryPath, ignore_errors = True, onerror = None)
        os.makedirs(currentDirectoryPath)
    except Exception as e:
        return(e)

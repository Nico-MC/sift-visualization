import os, re, uuid, glob, cv2 as cv, numpy as np
from flask import Blueprint, jsonify, abort

get_filenames = Blueprint('get_filenames', __name__)

@get_filenames.route('/get_filenames/<filename>', methods=['GET'])
def sift_cli_get_scales(filename):
    if(filename == 'original'):
        return get_output_files_of("original")
    elif(filename == 'dog'):
        return get_output_files_of("dog")
    elif(filename == 'scalespace'):
        return get_output_files_of("scalespace")
    else:
        abort(400, 'No such filename')

def get_output_files_of(directory):
    if(directory == 'scalespace'):
        filelist = os.listdir("static/scalespace")
        octaveList = []
        scalespace = {}
        for file in filelist:
            octave = re.search('(?<=_o).*(?=_)', file)
            if(scalespace.get(int(octave.group())) == None):
                scalespace[int(octave.group())] = ['http://localhost:5000/static/scalespace/' + file]
            else:
                scalespace[int(octave.group())].append('http://localhost:5000/static/scalespace/' + file)
            octaveList.append(int(octave.group(0)))
        scalespaceWithUniqueKey = {
            'scalespace': scalespace,
            'randomUuid': uuid.uuid4()
        }
        return(jsonify(scalespaceWithUniqueKey))
    elif(directory == 'dog'):
        filelist = os.listdir("static/dog")
        octaveList = []
        dogs = {}
        for file in filelist:
            octave = re.search('(?<=_o).*(?=_)', file)
            if(dogs.get(int(octave.group())) == None):
                dogs[int(octave.group())] = ['http://localhost:5000/static/dog/' + file]
            else:
                dogs[int(octave.group())].append('http://localhost:5000/static/dog/' + file)
            octaveList.append(int(octave.group(0)))
        dogsWithUniqueKey = {
            'dogs': dogs,
            'randomUuid': uuid.uuid4()
        }
        return(jsonify(dogsWithUniqueKey))





@get_filenames.route('/get_filenames/keypoints/', methods=['GET'])
def sift_cli_get_keypoints():
    return jsonify({
        "keypoints": {
            "original": get_keypoint_output_files_of("Original"),
            "dog": get_keypoint_output_files_of("DoG"),
            "scalespace": get_keypoint_output_files_of("Scalespace")
        },
        "randomUuid": uuid.uuid4()
    })

def get_keypoint_output_files_of(type):
    output_files = {}
    listing = glob.glob('static/keypoints/step*')
    for step_number, step in enumerate(listing):
        output_files[step_number] = {}
        listing = glob.glob(step + "/Octave*/" + type + "/")
        for octave_fileString in listing:
            octave_number = re.search('(?<=Octave_).*?(?=/)', octave_fileString).group()
            if(bool(output_files[step_number])):
                output_files[step_number].update({ octave_number: {} })
            else:
                output_files[step_number] = { octave_number: {} }

            listing = glob.glob(octave_fileString + "scale*")
            for scale_fileString in listing:
                scale_number = re.search('(?<=scale_).*(?=.jpg)', scale_fileString).group()
                output_files[step_number][octave_number][scale_number] = 'http://localhost:5000/' + scale_fileString

    return output_files

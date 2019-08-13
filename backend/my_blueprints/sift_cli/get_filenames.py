import os, re, uuid
from flask import Blueprint, jsonify, abort

get_filenames = Blueprint('get_filenames', __name__)

@get_filenames.route('/get_filenames/<filename>', methods=['GET'])
def sift_cli_get_scales(filename):
    if(filename == 'scalespace'):
        return get_output_files_of("scalespace")
    elif(filename == 'dog'):
        return get_output_files_of("dog")
    else:
        abort(400, 'No such filename')

@get_filenames.route('/get_keypoints/<inputImage_name>', methods=['GET'])
def sift_cli_get_keypoints(inputImage_name):
    if(inputImage_name != ''):
        inputImage_name = re.search('.*(?=.png)', inputImage_name).group()
        KeypointsWithUniqueKey = {
            'keypoints': inputImage_name + '.jpg',
            'randomUuid': uuid.uuid4()
        }
        return(jsonify(KeypointsWithUniqueKey))
    else:
        abort(400, 'No such filename')

def get_output_files_of(directory):
    if(directory == 'scalespace'):
        filelist = os.listdir("static/scalespace")
        octaveList = []
        scalespace = {}
        for file in filelist:
            octave = re.search('(?<=_o).*(?=_)', file)
            if(scalespace.get(octave.group()) == None):
                # scalespace[octave.group()] = [file] // We don't need the first (supporting) scale
                scalespace[octave.group()] = []
            else:
                scalespace[octave.group()].append(file)
            octaveList.append(octave.group(0))
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
            if(dogs.get(octave.group()) == None):
                dogs[octave.group()] = [file]
            else:
                dogs[octave.group()].append(file)
            octaveList.append(octave.group(0))
        dogsWithUniqueKey = {
            'dogs': dogs,
            'randomUuid': uuid.uuid4()
        }
        return(jsonify(dogsWithUniqueKey))

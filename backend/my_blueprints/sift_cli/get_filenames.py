import os, re, uuid
from flask import Blueprint, jsonify, abort

get_filenames = Blueprint('get_filenames', __name__)

@get_filenames.route('/get_filenames/<filename>', methods=['GET'])
def sift_cli_get_scalespace(filename):
    if(filename == 'scalespace'):
        return list_output_files_of("scalespace")
    elif(filename == 'dog'):
        return list_output_files_of("dog")
    else:
        abort(400, 'No such filename')

def list_output_files_of(directory):
    if(directory == 'scalespace'):
        filelist = os.listdir("static/scalespace")
        octaveList = []
        scalespace = {}
        for file in filelist:
            octave = re.search('(?<=_o).*(?=_)', file)
            if(scalespace.get(octave.group()) == None):
                scalespace[octave.group()] = [file]
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
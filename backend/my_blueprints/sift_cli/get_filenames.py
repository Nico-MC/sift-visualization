import os, re, uuid
from flask import Blueprint, jsonify

get_filenames = Blueprint('get_filenames', __name__)

@get_filenames.route('/get_filenames/<filename>', methods=['GET'])
def sift_cli_get_scalespace(filename):
    if(filename == 'scalespace'):
        return list_output_files_of("scalespace")
    if(filename == 'dog'):
        return list_output_files_of("dog")

def list_output_files_of(directory):
    if(directory == 'scalespace'):
        filelist = os.listdir("static/scalespace")
        octaveList = []
        scalespace = {}
        for file in filelist:
            octave = re.search('(?<=o).*(?=_)', file)
            if(scalespace.get(octave.group()) == None):
                scalespace[octave.group()] = [file]
            else:
                scalespace[octave.group()].append(file)
            octaveList.append(octave.group(0))
        scalespaceWithIndex = {
            'scalespace': scalespace,
            'randomUuid': uuid.uuid4()
        }
        return(jsonify(scalespaceWithIndex))

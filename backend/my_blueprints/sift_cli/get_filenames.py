import os, re, uuid, glob
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

@get_filenames.route('/get_keypoints', methods=['GET'])
def sift_cli_get_keypoints():
    output_files = {}
    listing = glob.glob('static/keypoints/step*')
    for step_number, step in enumerate(listing):
        output_files[step_number] = {}
        listing = glob.glob(step + "/Octave*")
        for octave_number, octave in enumerate(listing):
            if(bool(output_files[step_number])):
                output_files[step_number].update({ octave_number: {} })
            else:
                output_files[step_number] = { octave_number: {} }
            listing = glob.glob(octave + "/scale*")
            for scale_number, scale in enumerate(listing):
                scaleImage = {
                    'scale': scale,
                    'randomUuid': uuid.uuid4()
                }
                output_files[step_number][octave_number][scale_number] = (scaleImage)

    print(output_files)
    return jsonify(output_files)

def get_output_files_of(directory):
    if(directory == 'scalespace'):
        filelist = os.listdir("static/scalespace")
        octaveList = []
        scalespace = {}
        for file in filelist:
            octave = re.search('(?<=_o).*(?=_)', file)
            if(scalespace.get(octave.group()) == None):
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

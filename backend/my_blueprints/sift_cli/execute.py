#!/usr/bin/env python3
import os, subprocess, shutil, re
from flask import request, Blueprint, current_app as app
from werkzeug.utils import secure_filename
from .handle_keypoints import handle_keypoints

execute = Blueprint('execute', __name__)

@execute.route('/execute', methods=['GET'])
def sift_cli():
    # ---Arrange---
    inputImage_path = app.config["ASSETS_FOLDER"] + '/' + request.args.get('inputImage_name')
    ss_noct = request.args.get('ss_noct')
    ss_nspo = request.args.get('ss_nspo')
    ss_dmin = request.args.get('ss_dmin')
    ss_smin = request.args.get('ss_smin')
    ss_sin = request.args.get('ss_sin')
    thresh_dog = request.args.get('thresh_dog')
    thresh_edge = request.args.get('thresh_edge')
    ori_nbins = request.args.get('ori_nbins')
    ori_thresh = request.args.get('ori_thresh')
    ori_lambda = request.args.get('ori_lambda')
    descr_nhist = request.args.get('descr_nhist')
    descr_nori = request.args.get('descr_nori')
    descr_lambda = request.args.get('descr_lambda')
    verb_keys = request.args.get('verb_keys')
    verb_ss = request.args.get('verb_ss')

    sift_cli_params = \
    [
        "./demo_SIFT/bin/sift_cli", inputImage_path,     # algorithm executable and input picture
        "-ss_noct", ss_noct,    # number of octaves
        "-ss_nspo", ss_nspo,    # number of scales per octave
        "-ss_dmin", ss_dmin,    # the sampling distance in the first octave
        "-ss_smin", ss_smin,    # blur level on the seed image
        "-ss_sin", ss_sin,    # assumed level of blur in the input image
        "-thresh_dog", thresh_dog,    # threshold over the DoG response
        "-thresh_edge", thresh_edge,    # threshold over the ratio of principal curvature
        "-ori_nbins", ori_nbins,    # number of bins in the orientation histogram
        "-ori_thresh", ori_thresh,    # threshold for considering local maxima in the orientation histogram
        "-ori_lambda", ori_lambda,    # sets how local is the analysis of the gradient distribution
        "-descr_nhist", descr_nhist,    # number of histograms per dimension
        "-descr_nori", descr_nori,    # number of bins in each histogram
        "-descr_lambda", descr_lambda,    # sets how local the descriptor is
    ]
    # labels for output
    if(verb_keys == "2"):
        sift_cli_params.extend(["-verb_keys", verb_keys])   # flag to output the intermediary sets of keypoints
    if(verb_ss == "1"):
        sift_cli_params.extend(["-verb_ss", verb_keys])   # flag to output the scalespaces (Gaussian and DoG)
        res = check_output_directory()

    # ---Act---
    process = subprocess.Popen(sift_cli_params, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if(stderr.decode("utf-8") != ''):
        return stderr
    elif(stdout.decode("utf-8") != ''):
        features_string = stdout.decode("utf-8")
        file = open("static/features.txt", "a")
        file.write(features_string)
        file.close()

        process = subprocess.Popen(["./demo_SIFT/bin/anatomy2lowe", "static/features.txt"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if(stderr.decode("utf-8") != ''):
            return stderr
        elif(stdout.decode("utf-8") != ''):
            features2lowe_string = stdout.decode("utf-8")
            file = open("static/features2lowe.txt", "a")
            file.write(stdout.decode("utf-8"))
            file.close()
        return handle_keypoints(features_string, inputImage_path)

    # # ---Act---
    # print(stdout)
    # process = subprocess.Popen(["./demo_SIFT/bin/anatomy2lowe", "static/test.txt"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # stdout, stderr = process.communicate()
    # return handle_keypoints(stdout.decode("utf-8"), inputImage_path)


def check_output_directory():
    try:
        shutil.rmtree('static/scalespace', ignore_errors = True, onerror = None)
        shutil.rmtree('static/dog', ignore_errors = True, onerror = None)
        shutil.rmtree('static/keypoints', ignore_errors = True, onerror = None)
        os.makedirs('static/scalespace')
        os.makedirs('static/dog')
        os.makedirs('static/keypoints')
        return("Output directory cleared.")
    except Exception as e:
        return(e)

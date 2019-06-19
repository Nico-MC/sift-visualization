#!/usr/bin/env python3
import os, subprocess, shutil, re
from flask import request, Blueprint, current_app as app
from werkzeug.utils import secure_filename

execute = Blueprint('execute', __name__)

@execute.route('/execute', methods=['GET'])
def sift_cli():
    # ---Arrange---
    inputImage_name = app.config["UPLOAD_FOLDER"] + '/' + request.args.get('inputImage_name')
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
        "./demo_SIFT/bin/sift_cli", inputImage_name,     # algorithm executable and input picture
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
    if(verb_keys == "1"):
        sift_cli_params.extend(["-verb_keys", "1"])   # flag to output the intermediary sets of keypoints
    if(verb_ss == "1"):
        sift_cli_params.extend(["-verb_ss", "1"])   # flag to output the scalespaces (Gaussian and DoG)
        res = check_output_directory()

    # ---Act---
    process = subprocess.Popen(sift_cli_params, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if(stderr.decode("utf-8") != ''):
        return stderr
    elif(stdout.decode("utf-8") != ''):
        return stdout


def check_output_directory():
    try:
        if(os.path.isdir('static/scalespace') == True):
            shutil.rmtree('static/scalespace')
        if(os.path.isdir('static/dog') == True):
            shutil.rmtree('static/dog')
        if(os.path.isdir('static/scalespace') == False):
            os.makedirs('static/scalespace')
        if(os.path.isdir('static/dog') == False):
            os.makedirs('static/dog')
        return("Output directory cleared.")
    except Exception as e:
        return(e)

#!/usr/bin/env python3
from ctypes import *
import numpy as np

libCalc = CDLL("./bin/sift_lib.so")

# call C function to check connection
libCalc.connect()

w = 512
h = 512
n = POINTER(c_int)
x = np.array(w*h*sizeof(c_float))

sift_compute_points = libCalc.sift_compute_points
sift_compute_points.argtypes = [POINTER(c_float), c_int, c_int, n]
sift_compute_points.restype = Structure

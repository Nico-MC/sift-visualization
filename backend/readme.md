# Manage pip dependencies

Generate a requirements file and then install from it in another environment.
> pip3 freeze > requirements.txt <br>
  pip3 install -r requirements.txt (but better use current requirements.txt of the repository)

Delete all .pyc files
> find . -name \\\*.pyc -delete

If you want to compile sift_cli of the demo_SIFT you can use
> gcc -std=c99 -o sift_cli sift_cli.c io_png.o lib_sift_anatomy.o
  lib_util.o lib_sift.o lib_keypoint.o lib_description.o lib_discrete.o
  lib_matching.o lib_scalespace.o lib_io_scalespace.o -lpng -lm

sift_cli output
> x, y, sigma, theta, octave, scale

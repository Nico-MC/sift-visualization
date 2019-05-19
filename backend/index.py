import subprocess

# TODO: Paramteres
proc = subprocess.Popen("./demo_SIFT/sift_cli", shell=True)
proc.wait()

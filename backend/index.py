import subprocess
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    proc = subprocess.Popen("./demo_SIFT/sift_cli", shell=True)
    proc.wait()

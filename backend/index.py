#!/usr/bin/env python
import subprocess
from flask import Flask, jsonify
from flask_cors import CORS


# configuration
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# define sift_cli endpoint
@app.route('/get', methods=['GET'])
def get():
    process = subprocess.Popen("./demo_SIFT/bin/sift_cli", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    print stderr
    return stderr

if __name__ == '__main__':
    app.run()

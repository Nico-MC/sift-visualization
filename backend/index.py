#!/usr/bin/env python3
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(__name__)
app.config['ASSETS_FOLDER'] = 'demo_SIFT/assets'
app.config['ALLOWED_EXTENSIONS'] = set(['png'])

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

from my_blueprints.blueprints_loader import *
register_blueprints(app)

if __name__ == '__main__':
    app.run()

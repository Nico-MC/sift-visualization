import os
from flask import Blueprint, request, abort, current_app as app
from werkzeug.utils import secure_filename

upload_image = Blueprint('upload_image', __name__)

@upload_image.route('/upload_image', methods=['POST'])
def sift_cli_upload_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            abort(400, 'File cant be found')
        file = request.files['file']
        if file.filename == '':
            abort(400, 'No selected file')
        elif(file and allowed_file(request.files['file'].filename)):
            file = request.files['file']
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(file.filename)))
            return file.filename
        else:
            abort(400, 'Only .png images are allowed')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

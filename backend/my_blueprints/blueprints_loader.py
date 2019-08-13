from flask import Blueprint
from .sift_cli.execute import execute
from .sift_cli.get_filenames import get_filenames
from .sift_cli.upload_image import upload_image
from .sift_cli.animate_keypoints import animate_keypoints

def register_blueprints(app):
    app.register_blueprint(execute, url_prefix="/sift_cli")
    app.register_blueprint(get_filenames, url_prefix="/sift_cli")
    app.register_blueprint(upload_image, url_prefix="/sift_cli")
    app.register_blueprint(animate_keypoints, url_prefix="/sift_cli")

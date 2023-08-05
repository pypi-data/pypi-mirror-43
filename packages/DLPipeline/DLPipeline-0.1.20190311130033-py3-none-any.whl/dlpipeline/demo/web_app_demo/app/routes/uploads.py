from flask import Blueprint, send_from_directory

from dlpipeline.demo.web_app_demo.app.config import UPLOAD_FOLDER

uploads = Blueprint('uploads', __name__, template_folder='templates')


@uploads.route('/<filename>')
def send_file(filename):
  return send_from_directory(UPLOAD_FOLDER,
                             filename)

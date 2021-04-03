from flask import Flask
import os

UPLOAD_FOLDER = 'static/uploads/'

# TEMPLATE_DIR = os.path.abspath('/templates')
# STATIC_DIR = os.path.abspath('/static')
app = Flask(__name__)
# app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
# app.static_folder = '/static'




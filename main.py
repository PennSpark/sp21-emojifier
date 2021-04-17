import os
from app import app
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template, Response, jsonify
from werkzeug.utils import secure_filename
from camera import VideoCamera
import cv2
import pickle
import numpy as np
import torchvision.transforms as transforms
from PIL import *
import io
import matplotlib.pyplot as plt

# ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# def allowed_file(filename):
# 	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def upload_form():
	return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_image():
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['file']
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
	if file:
		filename = secure_filename(file.filename)
		path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
		file.save(path)
		with open(path, 'rb') as file:
			image_bytes = file.read()
		transform_image(image_bytes=image_bytes)
		#print('upload_image filename: ' + filename)
		flash('Image successfully uploaded and displayed below')
		data_dict = {'rate':5, 'sales_in_first_month':200, 'sales_in_second_month':400}
		int_features = [int(x) for x in data_dict.values()]
		final_features = [np.array(int_features)]
		prediction = model.predict(final_features)
		output = round(prediction[0], 2)
		return render_template('upload.html', filename=filename, value=output)
	# else:
	# 	flash('Allowed image types are -> png, jpg, jpeg, gif')
	# 	return redirect(request.url)

def transform_image(image_bytes):
    my_transforms = transforms.Compose([transforms.Resize(255),
                                        transforms.CenterCrop(224),
                                        transforms.ToTensor(),
                                        transforms.Normalize(
                                            [0.485, 0.456, 0.406],
                                            [0.229, 0.224, 0.225])])
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    print("success!")
    print(image)
    # Returns a tensor
    tensor = my_transforms(image)
    print(tensor.shape)
    return tensor

@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == "__main__":
    app.run() 

# video_stream = VideoCamera()

# def gen(camera):
#     k = cv2.waitKey(1)
#     while True:
#         print(k)
#         frame = camera.get_frame()
#         k = cv2.waitKey(1)
#         if k == 27:
#             break
#         cv2.waitKey(100)
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
#     print("OOPS")

# @app.route('/video_feed')
# def video_feed():
#     return Response(gen(video_stream),
#         mimetype='multipart/x-mixed-replace; boundary=frame')

# if __name__ == '__main__':
#     app.run(host='127.0.0.1', debug=True,port="5000")
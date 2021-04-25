import os
from app import app
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template, Response, jsonify
from werkzeug.utils import secure_filename
import cv2
import pickle
import numpy as np
import torchvision.transforms as transforms
from PIL import *
import io
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

model = tf.keras.models.load_model('saved_model/my_model')
class_names = ['angry', 'disgusted', 'fearful', 'happy', 'neutral', 'sad', 'surprised']
img_height = 48
img_width = 48
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
		flash('No image selected')
		return redirect(request.url)
	if file:
		filename = secure_filename(file.filename)
		path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
		file.save(path)
		img = keras.preprocessing.image.load_img(
			path, target_size=(img_height, img_width, 1), color_mode='grayscale'
		)
		img_array = keras.preprocessing.image.img_to_array(img)
		img_array = tf.expand_dims(img_array, 0) # Create a batch

		predictions = model.predict(img_array)
		score = tf.nn.softmax(predictions[0])

		print(
			"This image most likely belongs to {} with a {:.2f} percent confidence."
			.format(class_names[np.argmax(score)], 100 * np.max(score))
		)
		flash('You as an emoji:')
		output = class_names[np.argmax(score)]
		if output == "happy":
			emoji = "😄"
		elif output == "sad":
			emoji = "😢"
		elif output == "neutral":
			emoji = "😐"
		elif output == "angry":
			emoji = "😡"
		elif output == "fearful":
			emoji = "😨"
		elif output == "surprised":
			emoji = "😮"
		else:
			emoji = "🤢"
		return render_template('upload.html', filename=filename, value=emoji)

@app.route('/display/<filename>')
def display_image(filename):
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == "__main__":
    app.run() 
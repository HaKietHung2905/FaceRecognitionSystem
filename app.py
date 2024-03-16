import os
import zipfile
from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
from io import BytesIO
from datetime import datetime
from werkzeug.utils import secure_filename

from deepface import DeepFace
from deepface.commons import package_utils, folder_utils
import functions.saveImages as saveImages
import functions.saveData as saveData

app = Flask(__name__)


@app.route('/')
def index():
    # Add your main function logic here
    return render_template('index.html')

@app.route('/query_form', methods=['POST'])
def submit_form():

    return 1
    # Redirect to the home page or any other page after processing the form
    # return redirect(url_for('index'))


@app.route('/upload_form', methods=['POST'])
def upload_form():

    if 'image_input' not in request.files:
        return "No file part"
    
    file = request.files['image_input']
    
    # If user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return "No selected file"
    
    image_path = saveImages.save_uploaded_image(file)

    instance = saveData.detect_images(image_path)

    saveData.connect_database('database', instance)

    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

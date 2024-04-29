import os
import zipfile
import json
from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
from io import BytesIO
from datetime import datetime
from werkzeug.utils import secure_filename

from deepface import DeepFace
from deepface.commons import package_utils, folder_utils
import functions.saveImages as saveImages
import functions.saveData as saveData
import functions.queryDataByString as queryDataByString
import functions.queryDataByImages as queryDataByImages
import functions.loadImages as loadImages

app = Flask(__name__)


@app.route('/')
def index():
    # Add your main function logic here
    return render_template('index.html')

@app.route('/query_form', methods=['POST'])
def submit_form():
    # Get the text input value
    query_input = request.form.get('text_input')

    image_paths = []

    if query_input != '':
        query = queryDataByString.get_sql_query(query_input)
        #print(query)
        #Exact_query
        select_index = query.find("SELECT")
        query = query[select_index:]
        print('Query:', query)
        results = queryDataByString.get_images_data('database', query)
        for result in results:
            paths = loadImages.load_images_with_name(result[0], 'static/uploads')
            image_paths.extend(paths)
    else:
        file = request.files['image_input']
        image_path = saveImages.save_uploaded_image(file, 'static/queryImages/')
        results = queryDataByImages.prediction_images(image_path)
        for result in results:
            img_name = result["img_name"]  # Extract img_name from the dictionary
            paths = loadImages.load_images_with_name(img_name, 'static/uploads')
            image_paths.extend(paths)

    

    


    # Get the images same as images input
        
    # Returning the image paths as JSON
    # return image_path
    #return image_paths
    # Redirect to the route that displays the images
    #return query
    return redirect(url_for('get_image_paths', image_paths=json.dumps(image_paths)))


@app.route('/get_image_paths')
def get_image_paths():
    # Retrieve the image paths from the query string
    image_paths = request.args.get('image_paths')
    image_paths = json.loads(image_paths)

    folder_path = 'uploads'  # Adjust this if your folder path is different

    # Extract image names from the paths
    image_names = [os.path.basename(path) for path in image_paths]
    query = request.args.get('query_string')
    #return image_names
    #return query
    return render_template('result.html', folder_path=folder_path, image_names=image_names, query = query)

@app.route('/upload_form', methods=['POST'])
def upload_form():

    if 'image_input' not in request.files:
        return "No file part"
    
    file = request.files['image_input']
    
    # If user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return "No selected file"
    
    image_path = saveImages.save_uploaded_image(file, 'static/uploads')

    instance = saveData.detect_images(image_path)

    saveData.connect_database('database', instance)

    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

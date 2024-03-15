import os
import zipfile
from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
from io import BytesIO
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def index():
    # Add your main function logic here
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_form():

    return 1
    # Redirect to the home page or any other page after processing the form
    # return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for
import os.path
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = './uploads'


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/annotate', methods=['POST'])
def annotate():
    print(request.files)
    if 'file' not in request.files:
        return 'No selected file'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    filename = file.filename
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return filename

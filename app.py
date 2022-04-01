from flask import Flask, render_template, Response, request, send_file
import numpy as np
import face_recognition
from .src.camera import camera
from .src.database import DataBase
from .src.face import Face


app = Flask(__name__)


def Upload(name: str, file):
    db = DataBase()
    img = preprocess_image(file.read())
    location = face_recognition.face_locations(img)[0]
    face = Face.from_image(img, face_location=location, name=name)
    db.save_photos_to_db(face)
  

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        db = DataBase()
        name = request.form['name'].replace(' ', '')
        file = request.files['file'].read()
        face = Face.from_byte_string(file, name=name)
        print(str(face))
        db.save_photos_to_db([face])

    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    db = DataBase()
    faces = db.get_faces()
    return Response(camera(faces), mimetype='multipart/x-mixed-replace; boundary=frame')
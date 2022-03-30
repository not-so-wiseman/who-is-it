from flask import Flask, render_template, Response, request, send_file
from .src.camera import camera
from .src.database import DataBase
from .src.face import Face


app = Flask(__name__)


def Upload(name: str, file):
    print(file)
    #img = preprocess_image("{}\\{}".format(IMAGE_DIR, img))
    #location = face_recognition.face_locations(img)[0]
    #face = Face.from_image(img, face_location=location, name=name)
    #db.save_photos_to_db(face)
  

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        print(request.files)
        name = request.files['name'].replace(' ', '')
        file = request.files['file']
        Upload(name, file)
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    db = DataBase()
    faces = db.get_faces()
    return Response(camera(faces), mimetype='multipart/x-mixed-replace; boundary=frame')
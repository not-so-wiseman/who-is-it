from flask import Flask, render_template, Response
from flask_wtf import FlaskForm
from .src.camera import camera
from .src.database import DataBase
from .src.camera import camera

app = Flask(__name__)


class UploadFileForm(FlaskForm):
    file = FileField("File")
    submit = SubmitForm("Upload File")

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        file = request.files['file']
    return render_template('index.html', form=form)


@app.route('/video_feed')
def video_feed():
    db = DataBase()
    faces = db.get_faces()
    return Response(camera(faces), mimetype='multipart/x-mixed-replace; boundary=frame')
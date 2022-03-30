import os
import face_recognition
from src.database import DataBase
from src.face import Face
from src.utils import preprocess_image

DATABASE = "D:\MUN\Term8\8410ComputerVision\Project\who-is-it\data\images.db"
IMAGE_DIR = ".\data\images"

if os.path.exists(DATABASE):
    db = DataBase()
    db.send_command('''CREATE TABLE images (encoding, name, location)''')
    faces = []

    for img in os.listdir(IMAGE_DIR):
        name = img.split("_")[0]
        img = preprocess_image("{}\\{}".format(IMAGE_DIR, img))
        location = face_recognition.face_locations(img)[0]
        
        face = Face.from_image(img, face_location=location, name=name)
        faces.append(face)

    db.save_photos_to_db(faces)
        
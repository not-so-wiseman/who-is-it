from inspect import istraceback
import sqlite3
from .face import Face

DATABASE = "D:\MUN\Term8\8410ComputerVision\Project\who-is-it\data\images.db"

class DataBase:
    def __init__(self):
        self.database = DATABASE

    def _open(self):
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()

    def _close(self):
        self.connection.close()

    def save_photos_to_db(self, faces: list):
        assert(isinstance(faces[0], Face))
        self._open()        

        for face in faces:
            encoding, name, location = face.to_data_base_str()
            command = "INSERT INTO images VALUES ('{}', '{}', '{}')".format(
                encoding, name, location
            )
            self.cursor.execute(command)

        self.connection.commit()
        self._close()

    def get_faces(self) -> list:
        self._open()
        faces = []

        for row in self.cursor.execute("SELECT * FROM images ORDER BY name"):
            faces.append(Face.from_database_entry(row))
        
        self._close()
        return faces

    def send_command(self, command: str):
        self._open()
        self.cursor.execute(command)
        self.connection.commit()
        self._close()

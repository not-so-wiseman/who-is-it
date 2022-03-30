from typing import Tuple
import numpy as np
import face_recognition


class Face:
    def __init__(self, name, face_location, encoding):
        self.name = name.upper()
        self.face_location = face_location
        self.encoding = encoding

    def from_image(img, face_location: Tuple, name=""):
        encoding: np.ndarray = face_recognition.face_encodings(img, [face_location])[0]
        #print("Face {} encoded".format(name), flush=True)
        return Face(name=name, face_location=face_location, encoding=encoding)

    def from_database_entry(data: Tuple):
        encoding = []
        for pt in data[0].split(" "):
            if (pt != ''):
                encoding.append(float(pt))
        encoding: np.ndarray = np.asarray(encoding, dtype=float)

        name: str = data[1]

        location = [int(pt) for pt in data[2].split(",")]
        location: Tuple = tuple(location)

        return Face(name=name, face_location=location, encoding=encoding)

    def set_name(self, name):
        self.name = name.upper()

    def __eq__(self, others: list) -> bool:
        encodings = [img.encoding for img in others] if isinstance(others, list) else [others.encoding]
        results = face_recognition.compare_faces(encodings, self.encoding)
        return all(results)

    def get_distances(self, others: list) -> list:
        encodings = [img.encoding for img in others] if isinstance(others, list) else [others.encoding]
        results = face_recognition.face_distance(encodings, self.encoding)
        return results

    def best_match(self, others: list):
        encodings = [img.encoding for img in others]
        results = face_recognition.face_distance(encodings, self.encoding)
        results = list(results)
        match_idx = results.index(min(results))
        return others[match_idx]

    def is_match(self, other):
        distance = self.get_distances(other)[0]
        return True if distance < 0.5 else False

    def to_data_base_str(self):
        encoding = str(self.encoding)[1:-1].replace("\n", " ")
        location = str(self.face_location)[1:-1]
        return encoding, self.name, location

import cv2
import numpy as np
import face_recognition
from typing import Tuple

class Colour:
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)



def highlight_face(img: np.ndarray, location: Tuple, name=""):
    y1, x2, y2, x1 = location
    cv2.rectangle(img, (x1, y1), (x2, y2), Colour.RED, 2)
    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), Colour.RED, cv2.FILLED)
    cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 0.5, Colour.WHITE, 1)
    return img

    

    


def preprocess_image(img, resize=0) -> np.ndarray:
    if isinstance(img, str):
        img = face_recognition.load_image_file(img)
    
    #assert(img, isinstance(np.ndarray))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    if resize != 0:
        img = cv2.resize(img, (0, 0), None, fx=resize, fy=resize)

    return img


def resize_location(location: Tuple, scale: int) -> Tuple:
    y1, x2, y2, x1 = location
    return (y1 * scale, x2 * scale, y2 * scale, x1 * scale)
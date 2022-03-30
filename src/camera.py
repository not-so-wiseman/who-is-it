import cv2
import face_recognition
import numpy as np

from .face import Face
from .utils import highlight_face, resize_location, preprocess_image
from .database import DataBase

IMAGE_DIR = "..\data\images\\"
RESIZE = 0.25

def camera(data: list):
    assert(isinstance(data[0], Face))
    
    print("Starting Video Capture")
    cap = cv2.VideoCapture(0)

    while True:
        success, img = cap.read()
        if success:
            # Resize capture of faster processing
            img_small: np.ndarray = preprocess_image(img, resize=RESIZE)
            faces_in_image = face_recognition.face_locations(img_small)

            for loc in faces_in_image:
                face = Face.from_image(img_small, loc)
                best_match: Face = face.best_match(data)

                if face.is_match(best_match):
                    location = resize_location(loc, int(1/RESIZE))
                    img = highlight_face(img, location, best_match.name)

            #cv2.imshow("Video Feed", img)
            ret, buffer = cv2.imencode('.jpg', img)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    # Release handle to the webcam
    cap.release()
    cv2.destroyAllWindows()
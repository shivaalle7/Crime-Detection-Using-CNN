import cv2
import os
import face_recognition

KNOWN_DIR = 'blacklist'

def load_known_faces():
    encodings = []
    names = []
    if not os.path.exists(KNOWN_DIR):
        return encodings, names
    for file in os.listdir(KNOWN_DIR):
        path = os.path.join(KNOWN_DIR, file)
        img = face_recognition.load_image_file(path)
        vals = face_recognition.face_encodings(img)
        if vals:
            encodings.append(vals[0])
            names.append(os.path.splitext(file)[0])
    return encodings, names
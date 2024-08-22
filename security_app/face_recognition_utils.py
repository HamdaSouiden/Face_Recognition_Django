import face_recognition
import numpy as np

def get_face_encoding(image_path):
    image = face_recognition.load_image_file(image_path)
    face_encodings = face_recognition.face_encodings(image)
    if face_encodings:
        return face_encodings[0]
    return None

def compare_faces(known_encoding, unknown_encoding):
    return face_recognition.compare_faces([known_encoding], unknown_encoding)[0]
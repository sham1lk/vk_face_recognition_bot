import PIL
import cv2
import face_recognition
import numpy


def find_face(img, friends):
    img = numpy.asarray(img)
    faces = face_recognition.face_locations(img)
    all_encodings = []
    for friend in friends:
        enc = face_recognition.face_encodings(friend[0])
        if len(enc) > 0:
            all_encodings.append(enc[0])
    for face in faces:
        # face_encoding = face_recognition.face_encodings(img, [face])
        # matches = face_recognition.compare_faces(
        #     all_encodings,
        #     face_encoding
        # )
        cv2.rectangle(img, (face[3], face[2]), (face[1], face[0]), (0, 255, 0), 2)
    return img

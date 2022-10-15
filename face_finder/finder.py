import PIL
import cv2
import face_recognition
import numpy
import numpy as np


def find_face(img, friends):
    img = numpy.asarray(img)
    faces = face_recognition.face_locations(img)
    all_encodings = []
    friends_name = []
    for friend in friends:
        enc = face_recognition.face_encodings(friend[0])
        if len(enc) > 0:
            all_encodings.append(enc[0])
            friends_name.append(friend[1])
    for face in faces:
        enc = face_recognition.face_encodings(img, [face])[0]
        enc = face_recognition.face_distance(enc, all_encodings)
        if max(enc) > 0.86:
            print(enc)
            (i,) = np.where(np.isclose(enc, max(enc)))
            name = friends_name[i[0]]
            img = cv2.putText(
                img,
                name,
                (face[3], face[2]),
                cv2.FONT_HERSHEY_COMPLEX,
                1,
                (255, 0, 255),
                2,
                cv2.LINE_AA,
            )
        cv2.rectangle(img, (face[3], face[2]), (face[1], face[0]), (0, 255, 0), 2)
    return img

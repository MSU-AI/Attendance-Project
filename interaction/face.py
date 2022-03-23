"""This module is responsible for the face recognition.
"""
import face_recognition as fr
import numpy as np

class FaceClassifier:
    def __init__(self):
        pass

    def encode_face(self, std_frame, num_jitters=1, model='small'):
        """Returns encoded face - 128 dimension array per face of image
        Parameters
        ----------
        std_frame : numpy array
            standard frame of image
        The frame of the image that contains the face.
        """
        face_locations = fr.face_locations(std_frame)
        if len(face_locations) == 0:
            return
        face_encodings = fr.face_encodings(
            std_frame,
            face_locations,
            num_jitters=num_jitters,
            model=model,
        )
        if len(face_encodings) == 0:
            return
        return face_encodings[0]

    def find_best_matching_face_index(self, enc, list_of_encs):
        """Compares and returns the most similar face/encoding in list of 
        existing encoded faces.
        Parameters
        ----------
        enc : numpy array
            encoded face to compare
        list_of_encs : list of numpy arrays
            list of saved face encoding to compare with enc
        """
        best_index = -1
        min_dist = 99999
        for i, enc2 in enumerate(list_of_encs):
            dist = np.linalg.norm(enc - enc2)
            if dist < min_dist:
                min_dist = dist
                best_index = i
        return best_index

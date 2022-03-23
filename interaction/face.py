"""This module is responsible for the face recognition.
"""
import face_recognition as fr
import numpy as np


class Face:
    def __init__(self, std_frame, list_of_encs):
        """
        Parameters
        ----------
        std_frame : set of numpy arrays
            original image of face to identify
        list_of_encs : list of numpy arrays
            list of saved face encodings
        """
        self.std_frame = std_frame
        self.list_of_encs = list_of_encs

    def encode_face(std_frame):
        """Returns encoded face - 128 dimension array per face of image
        Parameters
        ----------
        std_frame : numpy array
            standard frame of image
        The frame of the image that contains the face.
        """
        face_locations = fr.face_locations(std_frame)
        face_encodings = fr.face_encodings(std_frame, face_locations)
        return face_encodings[0]

    def find_best_face(enc, list_of_encs):
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

"""This module is responsible for the face recognition.
"""
import pickle

import mediapipe as mp
import numpy as np
import pandas as pd

class Hand:
    gestures = [
        'unclassified',
        'number 1',
        'number 2',
        'number 3',
        'thumbs up',
        'thumbs down',
    ]

    def __init__(self, gesture, landmarks):
        """

        Parameters
        ----------
        gesture : str
            The gesture for the hand gesture, e.g. "thumbs up", "number 1", etc.
        landmarks : pandas.DataFrame
            The landmarks for the hand gesture. See
            https://github.com/MSU-AI/Attendance-Project/blob/master/hand-landmarks.png
            There should be 21 rows (landmarks) and 3 columns ((x, y, z)
            coordinates).
        """
        self.gesture = gesture
        self.landmarks = landmarks

    def __eq__(self, other):
        """
        Compare two hand gestures.
        """
        return self.gesture == other.gesture

    @classmethod
    def get_all_available_gestures(cls):
        """Returns all available hand gestures that are supported.

        Parameters
        ----------
        all_gesture_labels : list of str
            The list of all available hand gesture labels.
        """
        return cls.gestures
    
    def __str__(self):
        return f'Hand: {self.gesture}'


class MediapipeHands(mp.solutions.hands.Hands):
    """A helper class to interact with mediapipe Hands instance.

    See more at
    https://github.com/google/mediapipe/blob/v0.8.9/mediapipe/python/solutions/hands.py
    """

    def __init__(
        static_image_mode=True,
        max_num_hands=1,
        model_complexity=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    ):
        super().__init__(
            static_image_mode=static_image_mode,
            max_num_hands=max_num_hands,
            model_complexity=model_complexity,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )

    @staticmethod
    def get_landmark_index(landmark_name):
        return getattr(mp.solutions.hands.HandLandmark, landmark_name.upper()).value

    @staticmethod
    def get_landmark_name(landmark_index):
        return mp.solutions.hands.HandLandmark(landmark_index).name

    def landmarks_to_dataframe(self, one_hand_landmarks):
        """
        Parameters
        ----------
        one_hand_landmarks : an iterable of (x, y, z) coordinates
            Class instance
            ``mediapipe.framework.formats.landmark_pb2.NormalizedLandmarkList``.
            A more helpful explanation: This will be the iterable elements
            inside mediapipe solution outputs' ``multi_hand_landmarks`` field.
        """
        df = []
        for landmark_index, landmark in enumerate(one_hand_landmarks.landmark):
            df.append([
                landmark_index,
                landmark.x,
                landmark.y,
                landmark.z,
            ])
        df = pd.DataFrame(df, columns=['landmark_index', 'x', 'y', 'z'])
        df.set_index('landmark_index', inplace=True, drop=True)
        return df
    
    @classmethod
    def normalize_hand(self, df_hand, frame_shape):
        """
        Parameters
        ----------
        df_hand : landmarks in pandas.DataFrame
            The columns are 'x', 'y', 'z'.
        frame_shape : (height, width) or (height, width, channels)
            The shape of the frame. This is used to scale the y-coordinate
            into the unit of x-coordinate.
        """
        df = df_hand.copy()

        # rescale y to dimension to x
        df['y'] *= frame_shape[1] / frame_shape[0]

        # extract reference landmarks
        i_wrist = self.get_landmark_index('wrist')
        i_mid_mcp = self.get_landmark_index('middle_finger_mcp')
        i_ind_mcp = self.get_landmark_index('index_finger_mcp')

        # center wrist to zero
        df['x'] = df['x'] - df['x'][i_wrist]
        df['y'] = df['y'] - df['y'][i_wrist]
        df['z'] = df['z'] - df['z'][i_wrist]

        # define base unit, i.e. unit 1 after normalization
        base_unit = np.mean([
            np.linalg.norm(df.loc[i_mid_mcp] - df.loc[i_wrist]),
            np.linalg.norm(df.loc[i_ind_mcp] - df.loc[i_wrist]),
        ])

        # normalization
        df['x'] /= base_unit
        df['y'] /= base_unit
        df['z'] /= base_unit

        # switch signs for y and z
        # so that the y-axis is pointing up
        # and the z-axis would follow the right-hand rule (toward us)
        df['y'] *= -1
        df['z'] *= -1

        return df
    
    def process_frame(self, frame):
        """Wrapper around ``mediapipe.solutions.hands.Hands.process()``.

        Parameters
        ----------
        frame : numpy.ndarray, shape of (height, width, 3)
            The RGB frame to process.
        """
        outputs = self.process(frame)
        self.landmarks_list = []
        multi_hand_landmarks = outputs.multi_hand_landmarks or []
        for one_hand_landmarks in multi_hand_landmarks:
            df_hand = self.landmarks_to_dataframe(one_hand_landmarks)
            df_hand = self.normalize_hand(df_hand, frame.shape)
            self.landmarks_list.append(df_hand)
        return self.landmarks_list
    
    @property
    def n_hands_found(self):
        """Returns the number of hands found by Mediapipe.

        Maximum is limited by ``self.max_num_hands``.
        """
        return len(self.landmarks_list)
    
    def sort_landmarks(self):
        pass
    
    def get_best_landmarks(self):
        return self.landmarks_list[0]


class HandGestureClassifier:
    """A class that classifies hand gestures from normalized landmarks.
    """
    def __init__(self):
        self.model = self._read_in_trained_model()

    def _read_in_trained_model(self, path=None):
        if path is None:
            path = './interaction/model.pkl'
        with open(path, 'rb') as file:
            model = pickle.load(file)
        return model
    
    def predict(self, normed_landmarks):
        """
        Parameters
        ----------
        normed_landmarks : pandas.DataFrame
            The columns are 'x', 'y', 'z'. Landmarks are normalized according to
            ``MediapipeHands.normalize_hand()``.
        
        Returns
        -------
        hand : Hand instance
            The hand instance with predicted gesture.
        """
        x = normed_landmarks.to_numpy()[1:].flatten() # ignore the first row, wrist
        gesture_index = self.model.predict(x.reshape(1, -1))[0]
        gesture_name = Hand.gestures[gesture_index]
        return Hand(gesture_name, normed_landmarks)
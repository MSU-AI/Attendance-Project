#!/usr/bin/env python
import json
import pickle
import time

import cv2
import mediapipe as mp
import numpy as np
import pandas as pd

class HandTracker:
    def __init__(
        self,
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    ):
        """A class to identify the 21 landmarks of a hand using mediapipe.

        All the arguments are passed to
        `mediapipe.solutions.hands.Hands() <https://google.github.io/mediapipe/solutions/hands.html#configuration-options>`__.

        Parameters
        ----------
        static_image_mode : bool, default False
            If set to ``False``, the input images are treated as a video stream;
            if set to ``True``, the input images are treated as a static image,
            i.e.  the images are unrelated.
        max_num_hands : int, default 1
            The maximum number of hands to detect.
        min_detection_confidence : float, default 0.5
            The minimum detection confidence for the detection to be considered
            as a hand. Valid range is [0, 1].
        min_tracking_confidence : float, default 0.5
            Minimum confidence for tracking the hand in a video stream. Valid
            range is [0, 1]. Higher confidence means better tracking, at the
            cost of latency.
        """
        self.static_image_mode = static_image_mode
        self.max_num_hands = max_num_hands
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence
        self.mp_hands = mp.solutions.hands.Hands(
            static_image_mode=self.static_image_mode,
            max_num_hands=self.max_num_hands,
            min_detection_confidence=self.min_detection_confidence,
            min_tracking_confidence=self.min_tracking_confidence,
        )

        self.mp_draw = mp.solutions.drawing_utils
        self.solution_outputs = None

        with open('finger_index.json') as file:
            content = json.load(file)
            self.landmark_index = {
                name: id_ for id_, name in enumerate(content['index'])
            }
    
    def process_frame(self, frame):
        """Convert image frame into mediapipe Solution Outputs.

        This function updates ``self.solution_outputs``.

        Parameters
        ----------
        frame : numpy.ndarray of shape (H, W, 3)
            The image frame to be processed in RGB format.
        """
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.solution_outputs = self.mp_hands.process(rgb_image)
    
    def clear_solution_outputs(self):
        """Clear the mediapipe solution outputs.

        This function updates ``self.solution_outputs``.
        """
        self.solution_outputs = None

    def found_hand(self):
        """Check if at least one hand is found.

        Returns
        -------
        found_hand : bool
            True if at least one hand is found.
        """
        return self.solution_outputs.multi_hand_landmarks is not None
    
    def get_single_hand_dataframe(self, frame, hand_landmarks, normalize=True):
        """Return a pandas DataFrame of the hand landmarks.

        Parameters
        ----------
        frame : numpy.ndarray of shape (H, W, 3)
            The image frame to be processed in RGB format.
        hand_landmarks : mp.solutions.hands.HandLandmarks
            The hand landmarks to be converted into a pandas DataFrame.
        normalize : bool, default True
            If set to ``True``, the coordinates are normalized.
        
        Returns
        -------
        df : pandas.DataFrame
            The pandas DataFrame of the hand landmarks. Columns are 'x', 'y' and
            'z', indexed by the landmark indices.
        """
        df = []
        for id_, lm in enumerate(hand_landmarks.landmark):
            df.append([id_, lm.x, lm.y, lm.z])
        df = pd.DataFrame(df, columns=['id', 'x', 'y', 'z'])
        df.set_index('id', inplace=True, drop=True)
        return self.normalize_hand(frame, df) if normalize else df
    
    def get_all_hand_dataframes(self, frame, normalize=True):
        """Return a list of pandas DataFrames of the hand landmarks.

        Parameters
        ----------
        frame : numpy.ndarray of shape (H, W, 3)
            The image frame to be processed in RGB format.
        normalize : bool, default True
            If set to ``True``, the coordinates are normalized.
        
        Returns
        -------
        df_list : list of pandas.DataFrame
            The list of pandas DataFrames of the hand landmarks.
        """
        result = []
        for hand_landmarks in self.solution_outputs.multi_hand_landmarks:
            df = self.get_single_hand_dataframe(frame, hand_landmarks, normalize=normalize)
            result.append(df)
        return result

    def draw_single_hand(self, frame, hand_landmarks, *args, **kwargs):
        """Draw the hand landmarks on the image frame.

        Parameters
        ----------
        frame : numpy.ndarray of shape (H, W, 3)
            The image frame to be processed in RGB format.
        hand_landmarks : mp.solutions.hands.HandLandmarks
            The hand landmarks to be drawn.
        """
        self.mp_draw.draw_landmarks(
            frame, hand_landmarks,
            connections=mp.solutions.hands.HAND_CONNECTIONS,
            *args, **kwargs,
        )
    
    def draw_all_hands(self, frame, *args, **kwargs):
        """Draw all the hand landmarks on the image frame.

        Parameters
        ----------
        frame : numpy.ndarray of shape (H, W, 3)
            The image frame to be processed in RGB format.
        """
        for hand_landmarks in self.solution_outputs.multi_hand_landmarks:
            self.draw_single_hand(frame, hand_landmarks, *args, **kwargs)
    
    def normalize_hand(self, frame, hand):
        """Normalize the hand dataframe.

        This function does the following:
        - Setting aspect ratio to 1. This is especially important for frames
        that are not square.
        - Normalize all distances such that the average distance from the wrist
        to the middle finger MCP and index finger MCP is 1.
        - Flip y-axis and z-axis. So when viewing the image on monitor, +y is up
        and +z is toward the viewer.
        
        Parameters
        ----------
        frame : numpy.ndarray of shape (H, W, 3)
            The image frame to be processed in RGB format.
        hand : pandas.DataFrame
            The hand dataframe to be normalized. Columns are 'x', 'y', 'z'.
        
        Returns
        -------
        norm_hand : pandas.DataFrame
            The normalized hand dataframe. Columns are 'x', 'y', 'z'.
        """
        norm_hand = hand.copy()

        # rescale y to dimension of x
        norm_hand['y'] *= frame.shape[1] / frame.shape[0]

        # extract reference landmarks
        i_wrist = self.landmark_index['wrist']
        i_mid_mcp = self.landmark_index['middle_finger_mcp']
        i_ind_mcp = self.landmark_index['index_finger_mcp']

        # normalization
        norm_hand['x'] = norm_hand['x'] - norm_hand['x'][i_wrist]
        norm_hand['y'] = norm_hand['y'] - norm_hand['y'][i_wrist]
        base_unit = np.mean([
            np.linalg.norm(norm_hand.loc[i_mid_mcp] - norm_hand.loc[i_wrist]),
            np.linalg.norm(norm_hand.loc[i_ind_mcp] - norm_hand.loc[i_wrist]),
        ])
        norm_hand['x'] /= base_unit
        norm_hand['y'] /= base_unit
        norm_hand['z'] /= base_unit

        # switch signs if y and z
        norm_hand['y'] *= -1
        norm_hand['z'] *= -1

        return norm_hand
    
    def read_model(self, path):
        with open(path, 'rb') as file:
            self.model = pickle.load(file)

    def predict(self, df_hand):
        x = df_hand.to_numpy()[1:].flatten()
        return self.model.predict(x.reshape(1, -1))[0]

class OpencvCamera:
    def __init__(self, camera_id=0):
        self.capture = cv2.VideoCapture(camera_id)

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.capture.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    labels = np.array([
        'unclassified',
        'one', 'two', 'three',
        'thumbs up', 'thumbs down',
    ])

    hand_tracker = HandTracker(max_num_hands=1)
    hand_tracker.read_model('model.pkl')

    with OpencvCamera() as camera:
        while cv2.waitKey(1) != ord('q'):
            _, frame = camera.capture.read()
            frame = cv2.flip(frame, 1) # mirror

            hand_tracker.process_frame(frame)
            if hand_tracker.found_hand():
                df_hands = hand_tracker.get_all_hand_dataframes(frame)
                # hand_tracker.draw_all_hands(frame)

                for i_hand, df_hand in enumerate(df_hands):
                    label = labels[hand_tracker.predict(df_hand)]

                    # display prediction
                    lm = hand_tracker.solution_outputs.multi_hand_landmarks[i_hand].landmark
                    x_pixel = int(np.mean([lm[0].x, lm[9].x]) * frame.shape[1])
                    y_pixel = int(np.mean([lm[0].y, lm[9].y]) * frame.shape[0])
                    cv2.putText(
                        frame, label,
                        org=(x_pixel, y_pixel),
                        fontFace=cv2.FONT_HERSHEY_DUPLEX,
                        fontScale=0.5,
                        color=(0, 255, 0),
                    )
            hand_tracker.clear_solution_outputs()

            cv2.imshow(f'Hand gestures: {labels[1:]}', frame)
            time.sleep(0.03)

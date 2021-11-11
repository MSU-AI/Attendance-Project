#!/usr/bin/env python
import json
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
        """A class to identify the 21 knuckle points of a hand.
        All the arguments are passed to ``mediapipe.solutions.hands.Hands()``.
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

        with open('finger_index.json') as file:
            content = json.load(file)
            self.landmark_index = {
                name: id_ for id_, name in enumerate(content['index'])
            }
    
    def process_frame(self, frame):
        """Convert image frame into mediapipe Solution Outputs.
        Parameters
        ----------
        frame : numpy.ndarray of shape (H, W, 3)
            The image frame to be processed in RGB format.
        
        Returns
        -------
        processed_output : mediapipe.python.solution_base.SolutionOutputs
            The processed output of the mediapipe pipeline.
        """
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return self.mp_hands.process(rgb_image)
    
    @staticmethod
    def found_hand(mp_solution_outputs):
        """Check if at least one hand is found.
        Parameters
        ----------
        mp_solution_outputs : mediapipe.python.solution_base.SolutionOutputs
            The processed output of the mediapipe pipeline.
        Returns
        -------
        found_hand : bool
            True if a hand is found.
        """
        return mp_solution_outputs.multi_hand_landmarks is not None
    
    def get_single_hand_landmarks(self, frame, hand_landmarks, draw=False, normalize=True):
        if draw:
            self.mp_draw.draw_landmarks(
                frame, hand_landmarks,
                connections=mp.solutions.hands.HAND_CONNECTIONS,
            )

        df = []
        max_frame_dim = max(frame.shape[:2])
        for id_, lm in enumerate(hand_landmarks.landmark):
            df.append([id_, lm.x, lm.y, lm.z])
        df = pd.DataFrame(df, columns=['id', 'x', 'y', 'z'])
        df.set_index('id', inplace=True, drop=True)
        return self.normalize_hand(frame, df) if normalize else df
    
    def get_all_hands_landmarks(self, frame, outputs, draw=False, normalize=True):
        result = []
        for hand_landmarks in outputs.multi_hand_landmarks:
            df = self.get_single_hand_landmarks(
                frame,
                hand_landmarks,
                draw=draw,
                normalize=normalize,
            )
            result.append(df)
        return result
    
    def normalize_hand(self, frame, hand):
        norm_hand = hand.copy()

        # rescale y to dimension of x
        norm_hand['y'] *= frame.shape[1] / frame.shape[0]

        # extract reference landmarks
        i_wrist = self.landmark_index['wrist']
        i_mid_mcp = self.landmark_index['middle_finger_mcp']
        i_ind_mcp = self.landmark_index['index_finger_mcp']

        # normalization
        norm_hand['x'] = norm_hand['x'] - norm_hand['x'][i_wrist]
        norm_hand['y'] = -(norm_hand['y'] - norm_hand['y'][i_wrist])
        base_unit = np.mean([
            np.linalg.norm(norm_hand.loc[i_mid_mcp] - norm_hand.loc[i_wrist]),
            np.linalg.norm(norm_hand.loc[i_ind_mcp] - norm_hand.loc[i_wrist]),
        ])
        norm_hand['x'] /= base_unit
        norm_hand['y'] /= base_unit
        norm_hand['z'] /= base_unit
        return norm_hand
    
class OpencvCamera:
    def __init__(self, camera_id=0):
        self.capture = cv2.VideoCapture(camera_id)

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.capture.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    hand_tracker = HandTracker(max_num_hands=4)

    with OpencvCamera() as camera:
        while cv2.waitKey(1) != ord('q'):
            _, frame = camera.capture.read()
            frame = cv2.flip(frame, 1) # mirror

            outputs = hand_tracker.process_frame(frame)
            if hand_tracker.found_hand(outputs):
                hands_landmarks = hand_tracker.get_all_hands_landmarks(
                    frame,
                    outputs,
                    draw=True,
                    normalize=True,
                )

            cv2.imshow('Tracker for 21 hand landmarks', frame)
            time.sleep(0.02)

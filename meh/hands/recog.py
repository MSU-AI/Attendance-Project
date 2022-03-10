"""
Event handlers used for recognizing items in pictures!

We provide the HandRecognize and FaceRecognize handlers,
which will be bound to the IDs 'face' and 'hand' respectively.   
"""

import numpy as np
import io
import cv2
import PIL

from meh.hand import BaseHandler
from meh.formatters import Base64ImageFormatter, JSONFormatter

from recognition import HandTracker, SimpleFacerec


class HandRecognize(BaseHandler):
    """
    Attempts to recognize hand gestures in the given video frames.

    We are bound to the 'hand' ID.
    """
    
    ids=['hand']
    
    def __init__(self) -> None:
        
        super().__init__(name="HandRecognize", convert=Base64ImageFormatter(), revert=JSONFormatter())
        
    def start(self):
        
        # Create our hand tracker:

        self.hand_track = HandTracker(max_num_hands=1)
        self.hand_track.read_model('model.pkl')
        
        self.labels = np.array([
            'unclassified',
            'one', 'two', 'three',
            'thumbs up', 'thumbs down',
        ])

    def handle(self, data: bytes):
        """
        Checks for hand gestures in the given frame.
        
        We return a list of lables, and coordinates for each label.

        :param data: Frame to check
        :type data: bytes
        :return: Data of hand gestures
        :rtype: dict
        """
        
        # Convert the image into something we can use:

        img = np.array(PIL.Image.open(io.BytesIO(data)))

        # Flip the frame:

        frame = cv2.flip(img, 1)

        # Process the frame in the hand tracker:

        self.hand_track.process_frame(frame)

        # Check if a hand is found:

        final_lables = []

        if self.hand_track.found_hand():

            df_hands = self.hand_track.get_all_hand_dataframes(frame)

            for i_hand, df_hand in enumerate(df_hands):
                label = self.labels[self.hand_track.predict(df_hand)]

                # Append the label to the final lables:

                final_lables.append(label)
                
                # display prediction
                lm = self.hand_track.solution_outputs.multi_hand_landmarks[i_hand].landmark
                x_pixel = int(np.mean([lm[0].x, lm[9].x]) * frame.shape[1])
                y_pixel = int(np.mean([lm[0].y, lm[9].y]) * frame.shape[0])

                final_lables.append({
                    'label': label,
                    'x_cord': x_pixel,
                    'y_cord': y_pixel
                })
            
            self.hand_track.clear_solution_outputs()

        return final_lables


class FaceRecognize(BaseHandler):
    """
    Attempts to recognize faces in the given images.
    
    We are bound to the 'face' id.
    """
    
    ids=['face']
    
    def __init__(self) -> None:
        super().__init__(name="FaceRecognize", convert=Base64ImageFormatter(), revert=JSONFormatter())
    
    def start(self):
        """
        Create any necessary components.
        """
        
        # Create our face recognizer:

        self.face_rec = SimpleFacerec()
        self.face_rec.load_encoding_images("face_images/")
    
    def handle(self, data):
        """
        Process the given image and return faces found.
        
        We return the name of the face found,
        as well as it's position.

        :param data: Data to process
        :type data: bytes
        :return: Data about recognized faces
        :rtype: dict
        """
        
        # Convert the image into something we can use:

        img = np.array(PIL.Image.open(io.BytesIO(data)))

        # Flip the frame:

        frame = cv2.flip(img, 1)
        
        # Check if face is found:

        face_locations, face_names = self.face_rec.detect_known_faces(frame)

        # Return the data:

        return {
                'face_locations': face_locations.tolist(),
                'face_name': face_names,
        }

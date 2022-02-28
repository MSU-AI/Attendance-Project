"""
Handlers that are here for demo purposes.
"""

import io
import numpy as np
import cv2
import PIL
import traceback

from meh.hand import BaseHandler, PrintHandler, RaiseHandler
from meh.form import Base64ImageFormatter, BaseFormatter, JSONFormatter

from recognition import HandTracker, SimpleFacerec


class DummyHandler(BaseHandler):
    """
    DummyHandler, prints some basic stats about the data received.

    This handler has no practical purpose!
    It is only here to show how handlers are created,
    attributed to events, and how they return data to be processed.

    To get a response from this handler,
    send data under the ID 'dummy'!
    """

    ids = ["dummy"]

    def __init__(self):

        super().__init__(name='Dummy Handler', convert=BaseFormatter(), revert=JSONFormatter())

    def handle(self, data):
        """
        Just print data to show we are being handled.

        :param data: Data to be processed
        :type data: dict
        :return: Data to return
        :rtype: dict
        """

        print("Data: {}".format(data))

        # Send data back to client:

        return {
            'echo': data,
            'msg': 'This is the dummy handler'
        }


class DummyRaise(RaiseHandler):
    """
    DummyRaise - Raises an exception each time we are called.

    This is used to showcase the error handling 
    capabilities of MEHF.
    """

    ids=["error"]

    def __init__(self) -> None:
        super().__init__()

        self.exc = ValueError("This is a test!")


class ImageProcess(BaseHandler):
    """
    Processes the given image.

    We expect the image to be in Base64 format.
    """

    ids=["face"]

    def __init__(self) -> None:

        super().__init__(name='ImageProcess', convert=Base64ImageFormatter(), revert=JSONFormatter())

    def start(self):
        """
        Create any necessary components.
        """

        # Create our hand tracker:

        self.hand_track = HandTracker(max_num_hands=1)
        self.hand_track.read_model('model.pkl')

        # Create our face recognizer:

        self.face_rec = SimpleFacerec()
        self.face_rec.load_encoding_images("face_images/")

        self.labels = np.array([
            'unclassified',
            'one', 'two', 'three',
            'thumbs up', 'thumbs down',
        ])

    def handle(self, data) -> dict:
        """
        Process the image data and return some stats.

        :param data: Data to process
        :type data: bytes
        :return: Dictionary 
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
            # hand_tracker.draw_all_hands(frame)

            for i_hand, df_hand in enumerate(df_hands):
                label = self.labels[self.hand_track.predict(df_hand)]

                # Append the label to the final lables:

                final_lables.append(label)

                # display prediction
                lm = self.hand_track.solution_outputs.multi_hand_landmarks[i_hand].landmark
                x_pixel = int(np.mean([lm[0].x, lm[9].x]) * frame.shape[1])
                y_pixel = int(np.mean([lm[0].y, lm[9].y]) * frame.shape[0])
                cv2.putText(
                    frame, label,
                    org=(x_pixel, y_pixel),
                    fontFace=cv2.FONT_HERSHEY_DUPLEX,
                    fontScale=0.5,
                    color=(0, 255, 0),
                )
            self.hand_track.clear_solution_outputs()

        # Check if face is found:

        face_locations, face_names = self.face_rec.detect_known_faces(frame)

        # Draw rectangle and print names:

        for face_loc, name in zip(face_locations, face_names):

            y1,x1,y2,x2 = face_loc[0],face_loc[1],face_loc[2],face_loc[3]

            cv2.putText(frame,name,(x1,y1-10),cv2.FONT_HERSHEY_DUPLEX,1,(255,0,0),2)

            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,0,200),2)

            print("Found face!")

        print(face_locations)

        # Return the data:

        return {
                'face_locations': face_locations.tolist(),
                'face_name': face_names,
                'hand_lables': final_lables
        }


class DummyErrorHandler(PrintHandler):

    ids = [BaseException]

    def __init__(self) -> None:
        super().__init__(name='DummyErrorHandler', revert=JSONFormatter())

    def handle(self, data: dict):
        """
        Print the exception data and traceback,
        and send back some error data.

        :param data: Data of error
        :type data: dict
        :return: Nothing
        :rtype: None
        """

        print("Found error in MEH:")

        traceback.print_tb(data['excp'].__traceback__)

        print(data['excp'])

        return {
            'msg': 'We encountered an error!',
            'excp': str(data['excp'])
        }

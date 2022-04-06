"""
Event handlers used for recognizing items in pictures!

We provide the HandRecognize and FaceRecognize handlers,
which will be bound to the IDs 'face' and 'hand' respectively.   
"""

import numpy as np
import io
import PIL

from django.utils import timezone

from meh.hand import BaseHandler
from meh.formatters import Base64ImageFormatter, JSONFormatter

from interaction.frame_analyzer import FrameAnalyzer

from attendanceapp.models import Person, Group, AttendanceEvent

frame_ana = FrameAnalyzer()


class HandRecognize(BaseHandler):
    """
    Attempts to recognize hand gestures in the given video frames.

    We are bound to the 'hand' ID.
    """

    ids = ['hand']

    def __init__(self) -> None:

        super().__init__(name="HandRecognize", convert=Base64ImageFormatter(), revert=JSONFormatter())

        self.num = 0

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

        frame = np.array(PIL.Image.open(io.BytesIO(data)))

        # Load the frame into the analyzer:

        frame_ana.set_frame(frame, 'BGR')

        # Get the result:

        result = frame_ana.recognize_hand()

        print("Hand result: {}".format(result))
        print("Type: {}".format(type(result)))

        self.num += 1

        print(self.num)

        if result is None:
            
            # No result! Return nothing:
            
            return {'hand': None}

        return {
            'hand': result.gesture,
        }


class FaceRecognize(BaseHandler):
    """
    Attempts to recognize faces in the given images.

    We are bound to the 'face' id.
    """

    ids = ['face']

    def __init__(self) -> None:
        super().__init__(name="FaceRecognize", convert=Base64ImageFormatter(), revert=JSONFormatter())

    def start(self):
        """
        Create any necessary components.
        """
        
        # Load the face endcodings:

        self.encodings = []

    def handle(self, data: bytes):
        """
        Checks for hand gestures in the given frame.
        
        We return a list of lables, and coordinates for each label.

        :param data: Frame to check
        :type data: bytes
        :return: Data of hand gestures
        :rtype: dict
        """
        
        # This is probably inefficient!

        # Get the group we are working with:

        group = Group.objects.get(name=self.meta['group'] if 'group' in self.meta else 'ai')

        # Get list of people:

        people = group.person_set.all()

        encodings = []
        names = []

        for per in people:

            if not per.encodings:
                
                continue

            encodings.append(per.encodings)
            names.append(per.name)

        # Convert the image into something we can use:

        frame = np.array(PIL.Image.open(io.BytesIO(data)))

        # Load the frame into the analyzer:

        frame_ana.set_frame(frame, 'BGR')

        # Get the result:

        result = frame_ana.recognize_face(encodings)

        print(result)

        if result is None:

            # No face found! Return nothing:

            return {
                'name': 'unknown',
            }

        # Add a date event to the person:

        date = AttendanceEvent(person=names[result], event_date=timezone.now())

        date.save()

        return {
            'name': names[result].name
        }

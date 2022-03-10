"""This module contains the final APIs.

```python
import interaction.frame_analyzer as fa

frame = cv2.imread('path/to/image.jpg') # BGR format
analyzer = fa.FrameAnalyzer(frame)
analyzer.standardize_frame()
face = analyzer.identify_face()
hand = analyzer.identify_hand()
```
"""
import cv2

from .face import Face
from .hand import Hand

class FrameAnalyzer():
    """Class that analyzes image frame with AI models.

    Currently, it offers:
    - Hand gesture recognition
    - Face recognition
    """
    standard_colorspace = 'RGB'
    standard_size = (480, 480)

    def __init__(
        self,
        frame,
        rgb='RGB',
        standardize=True,
    ):
        """
        Initialize an instance of AnalyzeFrame.

        Parameters
        ----------
        frame : numpy.ndarray
            The frame to be analyzed.
        rgb : str, default 'RGB'
            The color space of the frame.
        standardize : bool, default True
            Whether to standardize the frame.
        """
        self.frame = frame
        self.rgb = rgb
        if standardize:
            pass
    
    @classmethod
    def standardize_frame_colorspace(cls, frame):
        """Convert the colorspace of self.frame into the standard.

        By default, functions like ``cv2.imread()`` reads in as BGR format.
        Whereas functions like ``matplotlib.pyplot.imshow()`` plots according to
        RGB format. Hence, it is good to standardize the colorspace that we use.

        Parameters
        ----------
        frame : numpy.ndarray
            The frame whose colorspace to be standardized.

        Returns
        -------
        frame : numpy.ndarray
            Frame in the standard colorspace.
        """
        pass
    
    @classmethod
    def standardize_frame_size(cls, frame):
        """Resize the frame to a standard size.

        Parameters
        ----------
        frame : numpy.ndarray
            The frame to be resized.

        Returns
        -------
        frame : numpy.ndarray
            Frame in the standard size.
        """
        pass

    @classmethod
    def standardize_frame(self, frame):
        """Standardize the frame.

        This is just a wrapper of all the standardization functions.
        """
        pass

    def recognize_all_hands(self):
        """Recognize all hands in the frame.

        Returns
        -------
        gestures : list
            The list of ``hand.HandGesture`` instances.
        """
        pass
    
    def recognize_hand(self):
        """Recognize the hand.

        In the case of multiple hands detected, it will...?

        Returns
        -------
        gesture : str
            The hand gesture.
        """
        pass

    def recognize_all_faces(self):
        """Recognize all faces in the frame.

        Returns
        -------
        faces : list
            The list of ``face.Face`` instances.
        """
        pass

    def recognize_face(self):
        """Recognize the face.

        In the case of multiple faces detected, it will...?

        Returns
        -------
        face : str
            The face.
        """
        pass
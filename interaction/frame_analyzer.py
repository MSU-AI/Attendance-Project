"""This module contains the final APIs.

```python
import cv2
from interaction.frame_analyzer import FrameAnalyzer

analyzer = FrameAnalyzer()

frame = cv2.imread('hand_images/thumbsup/image.jpg')
analyzer.set_frame(frame, 'BGR')
hand = analyzer.recognize_hand()
print(hand) # Hand: thumbs up

frame = cv2.imread('hand_images/1/image.jpg')
hand = analyzer.set_frame(frame, 'BGR').recognize_hand()
print(hand) # Hand: number 1
```
"""
import cv2

try:
    from . import face
    from . import hand
except ImportError:
    import face
    import hand

class FrameAnalyzer():
    """Class that analyzes image frame with AI models.

    Currently, it offers:
    - Hand gesture recognition
    - Face recognition
    """
    standard_colorspace = 'RGB'
    standard_size = (360, 360)

    def __init__(self, init_classifiers=True, init_mp_hands=True):
        """
        Initialize an instance of AnalyzeFrame.

        Parameters
        ----------
        init_classifiers : bool, default True
            Whether to initialize the classifiers, i.e. reading in the trained models.
        init_mp_hands : bool, default True
            Whether to initialize the hand.MediaPipeHands().
        """
        if init_classifiers:
            self.init_classifiers()
        if init_mp_hands:
            self.init_mp_hands()
    
    def set_frame(
        self,
        frame,
        rgb,
        standardize=True,
    ):
        """
        Initialize an instance of AnalyzeFrame.

        Parameters
        ----------
        frame : numpy.ndarray
            The frame to be analyzed.
        rgb : str, e.g. 'BGR' for ``cv2.imread()``
            The color space of the frame. Is there a way to detect from frame automatically?
        standardize : bool, default True
            Whether to standardize the frame.
        
        Returns
        -------
        self : ``FrameAnalyzer``
            The self instance.
        """
        self.frame = frame
        self.rgb = rgb
        if standardize:
            self.standardize_frame()
        return self
    
    @classmethod
    def standardize_frame_colorspace(cls, frame, input_colorspace):
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
        if input_colorspace == cls.standard_colorspace:
            return frame
        trans = getattr(cv2, f'COLOR_{input_colorspace}2{cls.standard_colorspace}')
        return cv2.cvtColor(frame, trans)

    @classmethod
    def _crop_landscape(cls, frame):
        shape_x, shape_y = frame.shape[1], frame.shape[0]
        if shape_x > shape_y:
            x0 = int((shape_x - shape_y) / 2)
            frame = frame[:, x0:x0+shape_y]
        return frame
    
    @classmethod
    def _resize_by_smaller(cls, frame, smaller_side_target_size=None):
        s_size = smaller_side_target_size
        if s_size is None:
            s_size = min(cls.standard_size)
        shape_x, shape_y = frame.shape[1], frame.shape[0]
        ratio = s_size / min(shape_x, shape_y)
        frame = cv2.resize(frame, (0, 0), fx=ratio, fy=ratio)
        return frame

    @classmethod
    def standardize_frame_size(cls, frame):
        """Resize the frame to a standard size.

        If frame is larger than the standard size, it will be shrinked.  If the
        frame is smaller than the standard size, it will be padded (not
        enlarged) with black background. The aspect ratio is always respected.
        Any remaining space will be filled with black.

        Parameters
        ----------
        frame : numpy.ndarray
            The frame to be resized.

        Returns
        -------
        frame : numpy.ndarray
            Frame in the standard size.
        """
        frame = cls._crop_landscape(frame)
        frame = cls._resize_by_smaller(frame)
        return frame

    def standardize_frame(self):
        """Standardize the frame.

        This is just a wrapper of all the standardization functions.
        """
        self.frame = self.standardize_frame_colorspace(self.frame, self.rgb)

    def init_classifiers(self):
        self.hand_classifier = hand.HandGestureClassifier()
        self.face_classifier = face.FaceClassifier()
    
    def init_mp_hands(self):
        self.mp_hands = hand.MediapipeHands()

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

        In the case of multiple hands detected, it will only return the best hand.

        Returns
        -------
        hand : ``hand.Hand instance`` or None
            If no hand is detected, returns None.
        """
        self.mp_hands.process_frame(self.frame)
        if self.mp_hands.n_hands_found > 0:
            best_landmarks = self.mp_hands.get_best_landmarks()
            return self.hand_classifier.predict(best_landmarks)

    def recognize_all_faces(self):
        """Recognize all faces in the frame.

        Returns
        -------
        faces : list
            The list of ``face.Face`` instances.
        """
        pass

    def recognize_face(self, list_of_encs):
        """Recognize the face.

        In the case of multiple faces detected, it will...?

        Returns
        -------
        face : str
            The face.
        """
        enc = self.face_classifier.encode_face(self.frame)
        if enc is not None:
            return self.face_classifier.find_best_matching_face_index(enc, list_of_encs)
    
    def _get_face_encoding(self, num_jitters=5, model='large'):
        return self.face_classifier.encode_face(self.frame, num_jitters=num_jitters, model=model)
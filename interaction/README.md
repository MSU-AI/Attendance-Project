# For non-coding team

Create a `.py` file right under the repository root:
```python
import cv2
from interaction.frame_analyzer import FrameAnalyzer

analyzer = FrameAnalyzer()
list_of_face_encodings = ... # have to query from database, e.g. SQL
list_of_names = ... # from database, too

frame = cv2.imread('test.jpg')
analyzer.set_frame(frame, 'BGR')
hand = analyzer.recognize_hand()
face_index = analyzer.recognize_face(list_of_face_encodings)
if face_index is None:
    print(hand) # Hand: thumbs up
else:
    print(hand, ',', list_of_names[face_index]) # Hand: thumbs up, John Doe
```

Remarks:
1. Submodule [interaction/frame_analyzer.py](interaction/frame_analyzer.py) should contain all the APIs you need, if not, please inform the coding team.
1. Face encoding is time-consuming. To save time, it is recommended to encode new face and store the encoded result into database for future query. Encoding face image is easy:
    ```python
    from interaction.frame_analyzer import FrameAnalyzer
    fa = FrameAnalyzer() # you can use existing FrameAnalyzer instance
    fa.set_frame(frame_with_face, 'BGR')
    enc = fa._get_face_encoding() # this is the API you need
    ```
    There are two common keyword arguments for face encoding, `num_jitters` and `model`. When storing new faces, if time permits, it is recommended to use `num_jitters=5` (or more) and `model='large'` for better accuracy but slower speed. You can tune down these two parameters, e.g. `num_jitters=1` and `model='small'`, to speed things up when feeding a stream of video frames. This faster mode is also the behavior of `FrameAnalyzer.recognize_face()`.



# For coding team

[`_app.py`](interaction/_app.py) is a script for the us to test if things are running as expected with our local computer. So everything is local. The face images will be put under [`face_images/`](interaction/face_images), an SQLite database file storing all the previously encoded faces will be saved as `data.db` (not committed), and the local webcam will be used to interact with users. None of these files nor directories should interfere with the external use (non-coding team), otherwise please report an issue.
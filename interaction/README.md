Create a `.py` file right under the repository root, `main.py`:
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

This will output:
```console
Hand: thumbs up
Hand: number 1
```
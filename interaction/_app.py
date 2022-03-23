import cv2
import time

try:
    from interaction.frame_analyzer import FrameAnalyzer
    from interaction import _database
except:
    from frame_analyzer import FrameAnalyzer
    import _database

LIST_OF_NAMES = None
LIST_OF_ENCS = None

def frame_routine(frame, analyzer):
    global LIST_OF_NAMES, LIST_OF_ENCS
    frame = cv2.flip(frame, 1) # flip frame horizontally, i.e. mirror

    analyzer.set_frame(frame, 'BGR')
    hand = analyzer.recognize_hand()
    face_index = analyzer.recognize_face(LIST_OF_ENCS)
    if face_index is None:
        print(hand)
    else:
        print(hand, LIST_OF_NAMES[face_index])
    time.sleep(0.02)
    cv2.imshow('frame', frame)

class OpencvCamera:
    def __init__(self, camera_id=0):
        self.capture = cv2.VideoCapture(camera_id)

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.capture.release()
        cv2.destroyAllWindows()
    
if __name__ == '__main__':
    face_encodings = _database.get_all_face_encodings()
    LIST_OF_NAMES = list(face_encodings.index)
    LIST_OF_ENCS = face_encodings.to_numpy()

    analyzer = FrameAnalyzer()
    with OpencvCamera() as camera:
        while cv2.waitKey(1) != ord('q'):
            _, frame = camera.capture.read()
            frame_routine(frame, analyzer)
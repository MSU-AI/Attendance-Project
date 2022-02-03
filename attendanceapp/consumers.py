import json
from channels.generic.websocket import WebsocketConsumer
from attendanceapp.models import Photo
from io import BytesIO
from binascii import a2b_base64

# The camera consumer takes image data from the webcam (sent over websockets)
# and sends back the processed metadata.

# Eventually, this is where code teams 1 and 2 will work their magic. But for
# now, it just returns a dumb placeholder value: the length of the string
# representing the encoded image.


class CameraConsumer(WebsocketConsumer):
    face_encodings = []

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        print("Disconnecting")
        pass

    def receive(self, text_data):
        """
        Here is where the magic happens.
        
        This function will be called upon each frame received.
        Ideally, we will run this through the algorithm 
        provided by the coding teams.
        
        In this case, we just return the length of the image.
        In production, we will likely send some info back,
        such as the name of the person we detected.

        :param text_data: Base64 string contaning the encoded image
        :type text_data: str
        """

        # Send back the text length:
        
        self.send(text_data=json.dumps({
            "length": len(text_data)
        }))

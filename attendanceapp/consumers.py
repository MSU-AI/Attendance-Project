import json
import base64
import io
import numpy as np
import cv2
import PIL
import time

from channels.generic.websocket import WebsocketConsumer
from attendanceapp.models import Photo


# Import the coding team stuff:

from recognition import HandTracker, SimpleFacerec

# The camera consumer takes image data from the webcam (sent over websockets)
# and sends back the processed metadata.

# Eventually, this is where code teams 1 and 2 will work their magic. But for
# now, it just returns a dumb placeholder value: the length of the string
# representing the encoded image.


class CameraConsumer(WebsocketConsumer):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Create our hand tracker:
        
        self.hand_track = HandTracker(max_num_hands=1)
        self.hand_track.read_model('model.pkl')
        
        # Create our face recongizer:
        
        self.face_rec = SimpleFacerec()
        self.face_rec.load_encoding_images("face_images/")
        
        self.labels = np.array([
            'unclassified',
            'one', 'two', 'three',
            'thumbs up', 'thumbs down',
        ])

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

        # Decode the Base64 string into an image:
                
        #img = np.array(PIL.Image.open(io.BytesIO(base64.b64decode(text_data))))
                        
        decoded_b64 = base64.b64decode(text_data.split(',')[1])
        
        #print(decoded_b64)
        
        img = PIL.Image.open(io.BytesIO(decoded_b64))
    
        img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
    
        # Flip the frame:

        frame = cv2.flip(img, 1)
                
        # Process the frame in the hand tracker:

        self.hand_track.process_frame(frame)

        # Check if a hand is found:
        
        final_lables = []

        if self.hand_track.found_hand():

            print("Found hands!")

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

        time.sleep(0.03)

        # Check if face is found:
        
        face_locations, face_names = self.face_rec.detect_known_faces(frame)

        # Draw rectangle and print names:
        
        for face_loc, name in zip(face_locations, face_names):
            
            y1,x1,y2,x2 = face_loc[0],face_loc[1],face_loc[2],face_loc[3]
            
            cv2.putText(frame,name,(x1,y1-10),cv2.FONT_HERSHEY_DUPLEX,1,(255,0,0),2)
            
            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,0,200),2)
            
            print("Found face!")

        # Return altered image:
        
        # self.send(json.dumps({
        #         'image': base64.b64encode(frame).decode()
        #     }))
        
        print(face_locations)
        
        self.send(json.dumps(
            {
                'face_locations': face_locations.tolist(),
                'face_name': face_names,
                'hand_lables': final_lables
            }
        ))

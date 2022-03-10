from cgitb import text
import json

from channels.generic.websocket import WebsocketConsumer

from meh.collection import HandlerCollection, parse_directory

# The camera consumer takes image data from the webcam (sent over websockets)
# and sends back the processed metadata.

# In this example, we create a HandlerCollection
# and load the relevant handlers.

# Create the HandlerCollection:

print("> Creating HandlerCollection ...")

hands = HandlerCollection()

# Load all handlers:

print("> Loading handlers ...")

parse_directory('meh/hands/', hands)

# Start all handlers:

print("> Starting all handlers ...")

hands.start_all()

# Print some stats, ideally later on we will
# Use a proper logging system, 
# But for now just printing to the terminal will do

print("+========================================+")
print("         --== [MEHF Status] ==--")
print("\nHandlers Loaded: [{}]".format(hands.num_loaded))

# Iterate over each handler:

for id, hand in hands.iter_handlers():

    # Print some info about said handler:

    print("ID: [{}] - Handler: [{}]".format(id, hand))

print("\n         --== [End MEHF Status] ==--")
print("+========================================+")


class CameraConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        print("Disconnecting")
        pass

    def receive(self, text_data):
        """
        Here is where the magic happens.

        This function will be called upon each frame received.
        We pass the data through MEHF and then return the result.

        :param text_data: Data to process
        :type text_data: str
        """

        index = text_data.index('}')

        # Process meta data:

        meta_text = text_data[0:text_data.index('}')+1]

        meta = json.loads(meta_text)

        # Send the data along:

        temp = hands.handle(meta['id'], text_data[index+1:])

        self.send(meta_text + temp)

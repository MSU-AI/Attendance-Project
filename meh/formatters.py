"""
This file contains formatters that are 
to be used with event handlers.

Event formatters are very simple:
They take an input and return an output.
Formatters usually change the state of the 
input data, and convert it into a new format.

One example of this is converting JSON strings
into valid python dicts to be used.
"""

import json
import base64


class BaseFormatter(object):
    """
    BaseFormatter - Class all formatters MUST inherit!

    This class defines some basic functionality that all
    formatters must implement.
    This class is very similar to a BaseHandler,
    the only difference being the 'convert' and 'revert' methods.

    'convert()' should convert arbitrary input data into something python can use.
    'revert()' should revert arbitrary output data into something that
    can be sent over a socket.
    """

    def convert(self, data):
        """
        Converts input data into something the EventHandler can understand.

        This method ideally should return a python dictionary,
        but the return data can be anything that the
        EventHandler can understand.

        We return the data we receive.

        :param data: Data to be converted
        :type data: Any
        :return: Data to be sent to the event handler
        :rtype: Any
        """

        return data

    def revert(self, data):
        """
        Reverts output data into something that can be sent over a websocket.

        This method ideally should return a string to be sent,
        but the return data can be anything that the 
        EventHandler can understand.args=

        We return the data we receive.

        :param data: Data to be reverted
        :type data: Any
        :return: Data to be sent over a socket
        :rtype: Any
        """

        return data


class JSONFormatter(BaseFormatter):
    """
    JSONFormatter - Converts and reverts data in JSON format!
    """

    def convert(self, data):
        """
        Converts input JSON data into a dictionary.

        :param data: Data to be converted
        :type data: str
        :return: Dictionary of data
        :rtype: dict
        """

        # Convert and return:

        return json.loads(data)

    def revert(self, data):
        """
        Reverts input dictionary into a JSON string.

        :param data: Data to be reverted
        :type data: dict
        :return: Reverted data
        :rtype: str
        """

        # Revert and return:

        return json.dumps(data)


class Base64Formatter(BaseFormatter):
    """
    Base64Formatter - Converts and reverts data in Base64!
    """

    def convert(self, data):
        """
        Converts Base64 strings into valid bytes to use.

        :param data: Base64 string to decode
        :type data: str
        :return: Byte data
        :rtype: bytes
        """

        return base64.b64decode(data)

    def revert(self, data):
        """
        Reverts the bytes into a Base64 object.

        :param data: Data to encode
        :type data: bytes
        :return: Base64 string
        :rtype: str
        """

        return base64.b64encode(data)


class Base64ImageFormatter(Base64Formatter):
    """
    Base64Formatter - Converts and reverts Base64 images!

    We are very similar as Base64Formatter,
    except that we strip the metadata.
    """

    def convert(self, data: str) -> bytes:
        """
        Strips the metadata and processes it.

        :param data: Data to be processed
        :type data: str
        :return: Bytes of the image
        :rtype: bytes
        """

        return super().convert(data.split(',')[1])

    def revert(self, data: bytes) -> str:
        """
        Converts the bytes and adds valid metadata.

        :param data: Data to be processed
        :type data: bytes
        :return: String of the Base64 image
        :rtype: str
        """

        return 'data:image/jpeg;base64,' + super().revert(data)

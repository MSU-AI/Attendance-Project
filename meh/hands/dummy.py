"""
Handlers that are here for demo purposes.
"""

import traceback

from meh.hand import BaseHandler, PrintHandler, RaiseHandler
from meh.formatters import BaseFormatter, JSONFormatter


class DummyHandler(BaseHandler):
    """
    DummyHandler, prints some basic stats about the data received.

    This handler has no practical purpose!
    It is only here to show how handlers are created,
    attributed to events, and how they return data to be processed.

    To get a response from this handler,
    send data under the ID 'dummy'!
    """

    ids = ["dummy"]

    def __init__(self):

        super().__init__(name='Dummy Handler', convert=BaseFormatter(), revert=JSONFormatter())

    def handle(self, data):
        """
        Just print data to show we are being handled.

        :param data: Data to be processed
        :type data: dict
        :return: Data to return
        :rtype: dict
        """

        print("Data: {}".format(data))

        # Send data back to client:

        return {
            'echo': data,
            'msg': 'This is the dummy handler'
        }


class DummyRaise(RaiseHandler):
    """
    DummyRaise - Raises an exception each time we are called.

    This is used to showcase the error handling 
    capabilities of MEHF.
    """

    ids=["error"]

    def __init__(self) -> None:
        super().__init__()

        self.exc = ValueError("This is a test!")


class DummyErrorHandler(PrintHandler):

    ids = [BaseException]

    def __init__(self) -> None:
        super().__init__(name='DummyErrorHandler', revert=JSONFormatter())

    def handle(self, data: dict):
        """
        Print the exception data and traceback,
        and send back some error data.

        :param data: Data of error
        :type data: dict
        :return: Nothing
        :rtype: None
        """

        print("Found error in MEH:")

        traceback.print_tb(data['excp'].__traceback__)

        print(data['excp'])

        return {
            'msg': 'We encountered an error!',
            'excp': str(data['excp'])
        }

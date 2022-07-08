"""
This file contains components that make using and working
with event handlers much easier.

The class in question is the HandlerCollection,
which manages multiple handlers, error management, 
and the handler state chain.

We also offer the 'parse_directory()' method,
which searches for valid handlers in the given
directory and loads them.
"""

from __future__ import annotations

import pkgutil
import inspect

from collections import defaultdict
from typing import Any, Tuple, Optional

from meh.hand import BaseHandler
from meh.errors import HandlerLoadError, HandlerStartError, HandlerStopError, HandlerUnloadError


class HandlerCollection(object):
    """
    HandlerCollection - Manages and works with handlers

    This class ties handlers to certain events,
    which will be called when certain data is received.
    We allow multiple handlers to be attached to the same event.

    This class also maintains the state chain of each handler,
    calling the start(), stop(), ect. methods when appropriate.

    A 'default handler' is an event handler that is to be called
    if we encounter event data that is not registered.
    All default handlers are stored under the key 'None'.
    You can attach as many default handlers as you wish.

    A 'global handler' is an event handler that is called
    every time valid data is encountered.
    Keep in mind, that if any unknown data is retrieved,
    then the global handlers will not be called.
    You can define a handler as global by using the GLOBAL constant.

    We also provide error handling for the attached event handlers.
    If an exception is encountered at any point when working with handlers,
    we pass the data, operation, and the troublemaker event handler
    to the relevant error handler for inspection.
    It is CRITICAL that no exceptions are raised for Django to see!
    Ideally, we should gracefully handle exceptions in the background,
    so the client connection does not get messed up.

    Error handlers will be given a dictionary with the following content:

    {
        'operation': String containing the handler operation,
        'data': Raw data from the socket, None if our operation is anything but 'handle',
        'excp': Exception that was raised during runtime 
    }

    If an error handler is registered under id of 'BaseException',
    then this handler will be registered as a global error handler.
    """

    GLOBAL = "GLOBAL"

    def __init__(self, hand_class: Any=BaseHandler) -> None:

        self.hand_class = hand_class  # Class that all handlers MUST inherit!
        self.hands = defaultdict(lambda: [])  # Dictionary of all handlers to use

        self.num_loaded = 0  # Number of handlers open
        self.max_num_loaded = 0  # Maximum number of handlers loaded
        self.empty = {}  # Empty response

    def reset(self):
        """
        Resets this HandlerCollection back to it's original state.

        This will remove all loaded handlers,
        default handlers, and all error handlers.

        Be warned, if not referenced elsewhere, 
        then these handler instances may be irreversibly deleted!
        """

        # Clear the handlers:

        self.hand_class.clear()

        # Clear the error handlers:

        self.errors.reset()

    def load_handler(self, hand: BaseHandler, ids: Optional[Tuple[str,...]]=None, extract: Optional[bool]=True) -> BaseHandler:
        """
        Adds the given handler to the collection.

        We ensure that the 'load' method of the handler is called,
        and that no exceptions are encountered.
        If we do encounter an exception,
        we do necessary error handling,
        and then we will not load this module!

        We also return the instance of the handler we loaded.

        By default, we extract the keys from each handler.
        Developers can optionally provide a list events
        that the handler can be bound to.
        Developers can also specify that they do not
        want the events bound within the handler to be loaded.

        If any errors are encountered, then they will be passed
        along to the relevant error handlers.
        This handler will NOT be loaded if any errors are encountered.

        This class can also be used to load error handlers!
        Just be sure to attach your error handler to the correct exceptions

        :param module: Handler to add
        :type module: BaseHandler
        :param ids: Extra IDs to bind the handler to
        :type ids: list
        :param extract: Boolean determining if we should extract IDs from the handler
        :type extract: bool
        :return: Handler we loaded
        :rtype: BaseHandler
        """

        # Do a check to ensure the handler is valid:

        if not isinstance(hand, self.hand_class):

            # Invalid handler!

            raise TypeError("Invalid handler! MUST inherit {}!".format(self.module_type))

        if ids is None:

            ids = []

        # Attach ourselves to the handler:

        hand.collection = self

        # We passed the check, let's run the load method:

        try:

            hand.load()

        except Exception as e:

            # Load error occurred! Do something about it!

            self.error_handle(HandlerLoadError, hand, None, 'load', e)
            
            return

        # Add the module to our collection:

        final_ids = ids

        if extract:

            final_ids = final_ids + hand.ids

        self._load_handler(hand, final_ids)

        # Finally, return the module:

        return hand

    def unload_handler(self, hand: BaseHandler) -> BaseHandler:
        """
        Removes the given handler from the collection.

        We ensure that the stop() and unload() methods are called as appropriate.
        if we do encounter an exception,
        then the handler will be forcefully unloaded,
        and no further methods(if any) will be called.
        We will also pass the error along to the error handlers.

        We first call the stop() method if the handler is running,
        and then finally the unload() method.
        After these methods do their work
        (Or if an exception is encountered),
        then we unload the handler from the collection.

        We also return a copy of the handler we unloaded.

        :param module: Handler to unload
        :type module: BaseHandler
        :return: Handler we unloaded
        :rtype: BaseModule
        """

        # Stop the handler if necessary:

        if hand.running:

            self.stop_handler(hand)
                
        # Now, run the unload method:

        try:

            hand.unload()

        except Exception as e:

            # Raise an exception of our own:

            self.error_handle(HandlerUnloadError, hand, None, 'unload', e)
            
            return

        # Unload the handler:

        self._unload_handler(hand)

        # Return the handler:

        return hand

    def stop_handler(self, hand: Any):
        """
        Stops the given handler.
        
        This is done by calling the handler's stop() method.
        We also return a copy of the module we worked with.

        If any errors are encountered,
        then we pass any exceptions through the relevant
        error handlers.

        :param module: Handler to stop
        :type module: BaseHandler
        :return: Handler we stopped
        :rtype: BaseHandler
        :raise: ModuleStopException: If the module stop() method fails
        """

        # Call the stop method:

        try:

            hand.stop()

        except Exception as e:

            # Raise an exception:

            self._unload_handler(hand)

            self.error_handle(HandlerStopError, hand, None, 'Stop', e)

        # Alter the running status:

        hand.running = False

        # Return the handler:

        return hand

    def start_handler(self, hand):
        """
        Starts the given handler.

        This is done by calling the start() method of the handler.
        We also return a copy of the handler we worked with.

        If we encounter any errors during the start operation,
        then we pass any exceptions to the relevant
        error handlers.

        :param module: Handler to start
        :type module: BaseHandler
        :return: Handler we started
        :rtype: BaseHandler
        """

        # Call the start method:

        try:

            hand.start()

        except Exception as e:

            # Handler failed to start! Unload it...

            self._unload_handler(hand)

            # Handle the exception:

            self.error_handle(HandlerStartError, hand, None, 'start', e)

        # Alter the running status:

        hand.running = True

        # Return the handler:

        return hand

    def restart_handler(self, hand):
        """
        Restarts the given handler.

        This is done by calling the start() and stop()
        methods of the handler in question.
        The handler MUST be in a running position to start!
        We also return the module we restarted.

        If any errors are encountered during the restart operation,
        then we pass the exception along to the relevant error handlers.

        :param module: Handler to restart
        :type module: BaseHandler
        :return: The handler we restarted
        :rtype: BaseHandler
        """

        # Stop the module

        self.stop_handler(hand)

        # Start the module:

        self.start_handler(hand)

        # Return the module in question:

        return hand

    def start_all(self):
        """
        Starts all loaded event handlers.
        """

        # Iterate over all handlers:

        for _, hand in self.iter_handlers():

            # Determine if the handler is running:

            if not hand.running:

                # Start the handler:

                self.start_handler(hand)

    def stop_all(self):
        """
        Stops all loaded event handlers.
        """

        # Iterate over all handlers:

        for _, hand in self.iter_handlers():

            # Determine if the handler is running:

            if hand.running:

                # Stop the handler:

                self.stop_handler(hand)

    def iter_handlers(self):
        """
        Iterates over each handler,
        and returns each once when encountered.

        We return the ID we are under,
        and the handler instance, respectively.

        This method is best used in a for loop.
        """

        # Iterate over each handler list:

        for key in self.hands.keys():

            # Iterate over each handler:

            for hand in self.hands[key]:

                # Yield each handler:

                yield key, hand

    def handle(self, id: str, data: Any, meta: dict) -> Any:
        """
        Sends the given data though the event handlers.

        The returned content is sent back to the client.

        If any errors are encountered,
        then they are sent through the error handlers,
        which have the option to change the state of the handler,
        HandlerCollection, or return data to be returned to the client.

        :param id: ID of the event
        :type id: str
        :param data: Data to be processed
        :type data: Any
        :param meta: Metadata for the given request
        :type meta: dict
        :return: Data to be sent back to the client
        :rtype: Any
        """

        # Get all handlers associated with the id:

        hands = self.hands[id]

        if not hands:

            # No registered handlers, use default ones:

            hands = hands + self.hands[None]

        else:

            # Also attach global handlers:

            hands = hands + self.hands[HandlerCollection.GLOBAL]

        # Run though each handler and process them:

        final_data = {}
        temp = None

        for hand in hands:

            try:

                temp = hand._meta_handle(data, meta)

            except Exception as e:

                # Handle the exception:

                temp = self.error_handle(e, hand, data, 'handle', e, meta)

            finally:

                if temp is not None:

                    # Add the data:

                    final_data = temp

        # Check if the data is nothing:

        if final_data is None:

            # Return generic empty response

            return self.empty

        # Otherwise return data:

        return final_data

    def error_handle(self, id: Exception, hand: BaseHandler, data: Any, oper: str, exc: Exception, meta: dict):
        """
        Handles the given exception.

        We are a bit different from conventional event handlers,
        in the sense that we search for class types.

        Default handlers are pulled from the handlers
        under the key 'BaseException'.

        :param id: Key exception to search under
        :type id: Exception
        :param hand: Handler to process
        :type hand: BaseHandler
        :param data: Data to be processed
        :type data: Any
        :param oper: Operation that was undergone
        :type oper: str
        :param exc: Exception to analyze
        :type exc: Exception
        :return: Data to send back to the client
        :rtype: Any
        """

        # Get all handlers affiliated with the exception

        hands = self.hands[type(id)]

        # Add default exception handlers:

        hands = hands + self.hands[BaseException]

        # Iterate over all exception handlers:

        final_data = {}

        for hand in hands:

            # Run the error handlers:

            temp = hand._meta_handle({
                'operation': oper,
                'data': data,
                'excp': exc
            }, meta)

            # Check if data is to be added:

            if temp:

                # Add data:

                final_data = temp

        return final_data

    def _load_handler(self, hand, ids):
        """
        Adds the handler to our collection. 

        This low-level method is not intended to
        be worked with by end users!

        :param mod: Module to add
        :type mod: BaseModule
        :param ids: List of events to bind the handler to
        :type ids: list
        :param extract: Boolean determining if we should extract IDs from the handler
        :type extract: bool
        """

        # Check if we received any IDs:

        if not ids:

            # No ids listed! Do not load...

            return 

        # Iterate over each ID:

        for id in ids:

            # Get the content:

            temp = self.hands[id]

            # Add the handler:

            temp.append(hand)

            # Finally, set the handler:

            self.hands[id] = temp

        # Update our stats:

        self.max_num_loaded += 1
        self.num_loaded += 1

        # Attach the collection to the module:

        hand.collection = self

    def _unload_handler(self, hand):
        """
        Low-level method for unloading handlers from the collection.

        We do not call any methods or work with the handler in any way
        other than removing it from the data structure.
        We will iterate over ALL handlers and remove the 
        given handler from all events.

        We are not meant to be called directly!
        This method should only be called by high-level
        methods of HandlerCollection.

        :param mod: The handler in question to remove
        :type mod: BaseHandler
        """

        # Iterate over all modules:

        for key, check in self.iter_handlers():

            # Check if we found a match:

            if hand == check:

                # Unload the handler:

                self.hands[key].remove(check)

        # Update our stats:

        self.num_loaded -= 1

        # Remove ourselves from the module:

        hand.collection = None


def parse_directory(path: str, final: HandlerCollection, hand_class: Any=BaseHandler) -> int:
    """
    Parses extensions from specified location.

    We make sure that all objects loaded inherit
    the class specified in the 'hand_class' argument.

    We also load the handlers into the given HandlerCollection.

    :param path: Path to directory location
    :type path: str
    :param final: HandlerCollection to add handler to
    :type final: HandlerCollection
    :return: Number of handlers loaded
    :rtype: int
    """

    # Iterating over every file in specified directory

    index = 0

    for finder, name, _ in pkgutil.iter_modules(path=[path]):

        # Loading module for inspection

        module = finder.find_module(name).load_module(name)

        for member in dir(module):

            # Iterating over builtin attributes

            obj = getattr(module, member)

            # Checking if extension is class

            if inspect.isclass(obj) and issubclass(obj, hand_class):

                # Create and load the handler:

                plug = obj()

                final.load_handler(plug)

                index += 1

    return index

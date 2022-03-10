"""
This file contains components for writing handlers.

The class of most intrest to most people is the BaseHandler,
which offers an abstract base class that people can use to create 
their own handlers that can be loaded into the HandlerCollection.

This file also contains other misc. handlers that may be useful in development!
"""

from meh.formatters import BaseFormatter


class BaseHandler(object):
    """
    BaseHandler - Class all handlers MUST inherit!

    A 'handler' is a component that is designed to handle a specific event.
    How the handler reacts to a given event is up the the handler,
    and depends on the specific use case.

    This class offers a framework for handlers,
    allowing for them to be identified, used, and worked with by the HandlerCollection.
    This also allows each handler to react to certain meta events,
    such as loading, starting, and stopping.

    Each module has a state that it can be in. Here is the state chain:

                      +<------------------------------<+
    Created -> Loaded +> Started -> Running -> Stopped +> Unloaded

    * Created - Module is instantiated
    * Loaded - Module is loaded into a collection, relevant load code is ran
    * Started - Module is started, relevant start code is ran 
    * Running - Module is running and working with data given to it via the 'handle()' method
    * Stopped - Module is stopped, relevant stop code is ran and module is no longer working with data
    * Unloaded - Module is unloaded, relevant unload code is ran

    This state chain shows each position a module can be in.
    Each state leads to the other, and the chain restarts if the module is unloaded.
    The exception to this rule is the stopped state,
    which can lead back to the started state if the module is started again.

    These states are reached by calling the relevant methods
    for the given module.
    These methods are usually called by some high-level class.
    Developers can add state event handling if their handler requires it!

    Each handler has two formatters that are used for converting and reverting.
    Event handlers can make set both parameters to the same formatter,
    but they can be diffrent if they wish.
    
    Handlers can define event ids that they should be attached to.
    These ids can be defined using the 'ids' class parameter.

    Event handlers MUST be loaded into a HandlerCollection class to be properly used!
    If these handlers are used discreetly, then certain components may fail to work.
    """

    ids = []  # List of IDs to bind this handler to

    def __init__(self, name='', convert=BaseFormatter(), revert=BaseFormatter()) -> None:

        self.name = name  # Friendly name of this module
        self.running = False  # Value determining if this module us running
        self.colllection = None  # Instance of the ModuleCollection we are bound to

        self.convert = convert  # Formatter used for conversion
        self.revert = revert  # Formatter used for reverting

    def start(self):
        """
        Method called when this event handler is started.

        This method is usually invoked by the HandlerCollection,
        but this can be invoked by a user if this handler
        is used discretely.

        Developers can really put anything they want in here,
        but is is recommended to start or invoke any components
        that are necessary for this handler's operation.
        """

        pass

    def stop(self):
        """
        Method called when this event handler is stopped.

        This method, like start(), is usually invoked by the 
        HandlerCollection, but this can be invoked by a developer
        if this handler is used discretely.

        Developers can really put anything they want in here,
        but it is recommended to stop all components in use by this handler,
        as it will stop working with events soon.

        Do not do anything too peraminit!
        This module may be started again at a later date,
        so ideally this handler should stop all components
        in a way that can be started again.
        """

        pass

    def load(self):
        """
        Method called when this event handler is loaded.

        This method is invoked when this handler is loaded 
        into a HandlerCollection.
        
        THIS DOES NOT MEAN THAT THE MODULE SHOULD GET READY FOR USE!

        That is the job of the start() method.
        Just because this module is loaded does not mean that it will be used.

        It is recommended to put basic startup code here,
        or define some parameters to change at load time.
        You probably should not start any major components in use
        until the start() method is called!
        """

        pass

    def unload(self):
        """
        Method called when this event handler is unloaded.

        This method is invoked when the module is unloaded from
        a HandlerCollection.
        When this method is called,
        it is reasonable to assume that this handler is not going to be used again.
        Event handlers can use this as a sign that their work is done.

        It is recommended to make any final, permanint changes once 
        this method is called.
        """

        pass

    def handle(self, data):
        """
        Method called when their is data to be handled.

        This data will usually consist of JSON data to work with,
        although some event handlers will use custom data fromats.

        We raise a NotImplementedError, as this functionality
        should be overridden in the child classes.

        This class should return data to be sent back to the client.
        If this method returns None, then we generate a generic
        'No Response' value, which is configurable by the HandlerCollection.

        :param data: Data to be processed
        :type data: Any
        """

        raise NotImplementedError("This method should be overridden in the child class!")

    def _meta_handle(self, data):
        """
        Meta handle method.

        This method does all the work
        of calling the formatters and the handle method.

        :param data: Data to be formatted
        :type data: Any
        :return: Data to be sent over a websocket
        :rtype: Any
        """

        # Convert the in data:

        conv = self.convert.convert(data)

        # Handle the in data:

        out = self.handle(conv)

        # Revert and return the data:

        return self.revert.revert(out)


class NullHandler(BaseHandler):
    """
    NullHandler - Does nothing!

    This is great for using as a placeholder,
    or if you want the default handler to do nothing.
    """

    def handle(self, data):
        """
        As promised, we do nothing.

        :param data: Data to not process
        :type data: Any
        """

        return None


class PrintHandler(BaseHandler):
    """
    PrintHandler - Prints the data to the terminal.

    We use the python 'print()' function,
    so the data will be redirected to stdout.
    """

    def handle(self, data):
        """
        Prints the data, as promised.

        :param data: Data to process
        :type data: Any
        """

        print(data)


class RaiseHandler(BaseHandler):
    """
    RaiseHandler - Raises an exception when called.

    This handler is great for raising errors when certain
    events are encountered.
    The exception raised can be customized to whatever you want.
    """

    def __init__(self) -> None:

        super().__init__('RaiseHandler')

        self.exc = None  # Exception to raise

    def handle(self, data):
        """
        Raises the given excpetion,
        as promised.

        :param data: Data to work with
        :type data: dict
        :return: Nothing! Just raise an exception
        :rtype: None
        """

        raise self.exc

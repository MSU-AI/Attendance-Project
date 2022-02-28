"""
Exceptions used by MEHF.

These exceptions are automatically raised when appropriate,
and can be used to attach error handlers to certain events. 
"""


class BaseMEHException(Exception):
    """
    BaseMEHException - Class all MEH excpetions should inherit!
    """

    pass


class HandlerLoadError(BaseMEHException):
    """
    HandlerLoadError - Raised when the load() method of a handler fails.
    """

    pass


class HandlerStartError(BaseMEHException):
    """
    HandlerStartError - Raised when the start() method of a handler fails.
    """

    pass


class HandlerStopError(BaseMEHException):
    """
    HandlerStopError - Raised when the stop() method of a handler fails.
    """

    pass


class HandlerUnloadError(BaseMEHException):
    """
    HandlerUnloadError - Raised when the unload() method of a handler fails.
    """

    pass

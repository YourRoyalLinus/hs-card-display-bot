
__all__ = (
    "APIException",
    "InvalidArgument", 
    "HTTPException",
    "APIServerError",
    "NoCardFound",
)

class APIException(Exception):
    """Base exception class for hearthstone api"""
    pass

class InvalidArgument(APIException):
    """Exception that's raised when an argument passed to an API calling
    function is not valid
    """
    pass

class HTTPException(APIException):
    """Exception that's raised when errors are recieved during requests
    to the API endpoints
    """

    def __init__(self, message, status):
        self.message = message
        self.status = status

        super().__init__(self.message)

class APIServerError(HTTPException):
    """Exception that's raised when a 500 range status code occurs

    Subclassed from :class:`HTTPExcpetion`
    """
    pass

class NoCardFound(HTTPException):
    """Exception that's raised when the API fails to return data from a user
    query to an endpoint that is expecting to return a CollectibleCard or
    NonCollectible Card object

    Subclassed from :class:`HTTPExcpetion`
    """
    pass
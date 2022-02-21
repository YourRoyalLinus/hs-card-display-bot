
__all__ = (
    "APIException", 
    "InvalidArgument",
    "NoCardFound",
    "NoCardbackFound",
    "NoDataFound"
)

class APIException(Exception):
    """Base exception class for hearthstone api"""
    pass

class InvalidArgument(APIException):
    """Exception that's raised when an argument passed to an API calling
    function is not valid
    
    E.g: 'partial_name' arg is None or empty in fetch_card_by_partial_name
    """
    pass

class NoCardFound(APIException):
    """Exception that is raised when the API fails to return data from a user
    query to an endpoint that is expecting to return a CollectibleCard or
    NonCollectible Card object
    """

class NoCardbackFound(APIException):
    """Exception that is raised when the API fails to return data from a user
    query to an endpoint that is expecting to return a Cardback object
    """
    pass

class NoDataFound(APIException):
    """Exception that is raised when an expected attribute of a concrete
    implemented _Card object is missing
    """
    pass
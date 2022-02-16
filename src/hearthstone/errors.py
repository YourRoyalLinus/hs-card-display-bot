
__all__ = (
    "APIException", 
    "InvalidArgument",
    "HTTPException", 
    "NoCardFound",
    "NoCardbackFound",
    "NoDataFound"
)

class APIException(Exception):
    pass

class InvalidArgument(APIException):
    pass

class HTTPException(APIException):
    pass

class NoCardFound(APIException):
    pass

class NoCardbackFound(APIException):
    pass

class NoDataFound(APIException):
    pass
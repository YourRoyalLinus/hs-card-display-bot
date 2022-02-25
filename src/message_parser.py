import re
from typing import Union, List
from discord import Message
from src._fetch_request import CardFetchRequest, MetadataFetchRequest

class ParserException(Exception):
    """Base exception raised when an error occurs while parsing"""
    def __init__(self, base: Exception):
        super().__init__()
        self.exception = base

class NoValidRequests(ParserException):
    """Exception that's raised when no valid fetch requests are found after
    parsing the message
    """
    pass

def is_valid_request_str(msg_content: str) -> bool:
    """Determine whether the :class:`Discord.Message` content has a proper 
    closing bracket for every valid open bracket. Valid brackets are either 
    `[]` or `{}`

    Positional Arguemnts:
        - msg_content : str
            - the text representation of the Discord.Message message
    
    Returns:
        `True` if there is a proper corresponding closing bracket for every
        valid opening bracket
    """
    _valid_brackets = {']':'[', '}':'{'}

    stack = []
    total_stack_count = 0
    for s in msg_content:
        if s in _valid_brackets.values(): 
            total_stack_count += 1
            stack.append(s)
        elif s in _valid_brackets.keys():
            i = stack.pop()
            if _valid_brackets[s] != i:
                return False
        else:
            continue
        
    return stack == [] and total_stack_count > 0

def _parse_message_str(msg_content :str) -> List[
                                                Union[
                                                    CardFetchRequest, 
                                                    MetadataFetchRequest
                                                ]
                                            ]:
    """Generate a :class:`FetchObject` for each valid NON-NESTED fetch request 
    found in the :class:`Discord.Message`. Valid fetch requests are wrapped in
    `[]` for :class:`CardFetchRequests` and `{}` for 
    :class:`MetadataFetchRequests`.
        - E.g: "[card_name] or {card_name} or [card_dbfid]" or "Man [card_name]
        and {other_card_name} are too strong right now!"
    
    Attempts to nest fetch requests - "[ [card_name] too good!]" will result in
    the first child request that matches the outer request to be invalid

    Positional Arguemnts:
        - msg_content : str
            - the text representation of the Discord.Message message
    
    Returns:
        a list of :class:`FetchRequest` objects

    """
    fetch_requests = []
    _brackets = [['[',']'], ['{','}']]

    for i in range(0, len(_brackets)):
        pattern = f"\{_brackets[i][0]}(.*?)\{_brackets[i][1]}"
        req = re.findall(pattern, msg_content) 
        if req and i == 0:
            fetch_requests.append(CardFetchRequest(req))
        elif req and i ==1:
            fetch_requests.append(MetadataFetchRequest(req))
        else:
            continue
        
    return fetch_requests 

def parse_message(msg :Message) -> List[Union[
                                            CardFetchRequest, 
                                            MetadataFetchRequest
                                        ]
                                    ]:
    """Generate a list of :class:`FetchRequest` objects from 
    :class:`Discord.Message`
    
    Positional Arguments:
        msg : Discord.Message
            - Message object that represents a message sent in a discord 
            server
            
    Returns
        list of :class:`FetchRequests` objects
    
    If there are no :class:`FetchRequest` objects, a `NoValidRequests` 
    exception is raised. Any other exception raises a `ParserException`
    """
    try:
        fetch_requests =  _parse_message_str(msg.content)
    except Exception as e:
        raise ParserException(e)
        
    if fetch_requests:
            return fetch_requests
    else:
        raise NoValidRequests("No valid fetch requests found in Message: "
                         f"{msg.content}")
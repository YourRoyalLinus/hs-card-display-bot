import re
from typing import Callable, Set, Tuple
from discord import Message
from _fetch_request import CardFetchRequest, MetadataFetchRequest

class ParserError(Exception):
    pass

def is_valid_request_str(msg_content: str) -> bool:
    _valid_brackets = {']':'[', ')':'(', '}':'{'}

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

def _parse_message_str(msg_content :str) -> list:
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

def parse_message(msg :Message) -> Tuple[Callable, Callable, Set[str]]:
    fetch_requests =  _parse_message_str(msg.content)
    if fetch_requests:
            return fetch_requests
    else:
        raise ParserError("No valid fetch requests found in Message: "
                         f"{msg.content}")
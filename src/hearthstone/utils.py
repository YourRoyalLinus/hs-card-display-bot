from typing import Any, Union
from .errors import NoCardFound, NoCardbackFound
from ._card import MultipleCards, NonCollectibleCard, CollectibleCard
from ._card import Cardback

def parse_api_result(api_result :Any) \
        -> Union[MultipleCards, Union[CollectibleCard, NonCollectibleCard]]:
    if type(api_result) is dict and api_result.get("error"):
        raise NoCardFound(api_result.get("message"))
    
    if len(api_result) > 1:
        return MultipleCards(api_result)
    else:
        try:
            collectible = api_result[0]["collectible"]
        except KeyError:
            collectible = False
    
    if collectible:
        return CollectibleCard(api_result[0])
    else:
        return NonCollectibleCard(api_result[0])

def parse_cardback_api_result(cardback_api_result :Any) \
                            -> Union[MultipleCards, Cardback]:
    if type(cardback_api_result) is dict \
        and cardback_api_result.get("error"):
        raise NoCardbackFound(cardback_api_result.get("message")) 
 
    if len(cardback_api_result) > 1:
        return MultipleCards(cardback_api_result)
    else:
        return Cardback(cardback_api_result[0])

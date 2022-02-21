from typing import Any, Union
from .errors import NoCardFound, NoCardbackFound
from ._card import MultipleCards, NonCollectibleCard, CollectibleCard
from ._card import Cardback

def parse_api_result(api_result :Any) \
        -> Union[MultipleCards, Union[CollectibleCard, NonCollectibleCard]]:
    """Parse the result returned by the API call and instantiate the proper
    concrete implementation of _Card by inspecting api_result

    Positional Arguments:
        - api_result : Any
            - the result of the call to the api endpoint. api_result could be 
            Any type but the expected proper form is a dict
    
    Raises NoCardFound exception if api_result.keys() contains an 'error' key

    Returns:
        a concrete _Card implemented class inferred from the api_result object
    """
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
    """Parse the result returned by a cardback fetching API call and 
    instantiate a Cardback object if len(cardback_api_result) == 1, or 
    MultipleCards otherwise

    Positional Arguments:
        - cardback_api_result : Any
            - the result of the call to an api endpoint that returns cardback
            data. cardback_api_result could be Any type but the expected proper
            form is a dict

    Raises NoCardFound exception if api_result.keys() contains an 'error' key

    Returns:
        Cardback object if len(cardback_api_result) == 1, or a MultipleCards 
        object otherwise
    """
    if type(cardback_api_result) is dict \
        and cardback_api_result.get("error"):
        raise NoCardbackFound(cardback_api_result.get("message")) 
 
    if len(cardback_api_result) > 1:
        return MultipleCards(cardback_api_result)
    else:
        return Cardback(cardback_api_result[0])

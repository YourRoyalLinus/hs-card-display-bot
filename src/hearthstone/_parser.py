from typing import Union
from ._card import MultipleCards, NonCollectibleCard, CollectibleCard, Cardback

def parse_api_result(api_result :dict) \
        -> Union[MultipleCards, Union[CollectibleCard, NonCollectibleCard]]:
    """Parse the result returned by the API call and instantiate the proper
    concrete implementation of _Card by inspecting api_result

    Positional Arguments:
        - api_result : dict
            - the result of the call to the api endpoint.
    
    Returns:
        a concrete _Card implemented class inferred from the api_result object
    """
    if len(api_result) > 1:
        return MultipleCards(api_result)
    else:
        try:
            collectible = api_result[0]["collectible"]
        except KeyError:
            collectible = False
        try:
            cardback = api_result[0]["cardBackId"]
        except KeyError:
            cardback = False
    
    if cardback:
        return Cardback(api_result[0])
    elif collectible:
        return CollectibleCard(api_result[0])
    else:
        return NonCollectibleCard(api_result[0])
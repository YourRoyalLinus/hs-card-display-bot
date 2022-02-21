import aiohttp
from typing import Any, Coroutine, Union
from cache import AsyncLRU

from .errors import InvalidArgument
from ._parser import parse_api_result, parse_cardback_api_result
from ._card import MultipleCards, CollectibleCard, NonCollectibleCard, Cardback
from ._api import ENV

_BASE_URL = ENV["API_URI"]
_HEADERS =  {
        'x-rapidapi-host': ENV["API_HOST"], 
        'x-rapidapi-key' : ENV["API_KEY"]
} 

async def _make_request(session :aiohttp.ClientSession, 
                        url :str, headers :dict, params :dict) -> Coroutine:
    """Make an asynchronous request using aiohttp.session.get passing
    url=url, headers=headers, params=params and return the result

    Positional Arguments:
        - session : aiohttp.ClientSession
            - a reference to the aiohttp client session
        - url : str
            - the API endpoint url, which is a combination of the _BASE_URL
            global module variable concatenated with an endpoint variable from
            each API function
        - headers : dict
            - the headers to be passed in. Every header includes the
            _HEADERS global module dict variable which contains API_HOST 
            and API_KEY keys, plus any new key:value pairs passed in from each
            API function
        - params : dict
            - keyword parameters to pass to session.get(). Recieved from
            the calling function as kwargs
    
    Returns:
        the Coroutine from awaiting request.json()
    """
    async with session.get(url=url, headers=headers, params=params) as req:
        response = await req.json()
    return response

@AsyncLRU(maxsize=128)
async def fetch_info(session :aiohttp.ClientSession, **kwargs) -> Any:
    """Make an asynchronous request to /info endpoint.

    Positional Arguments:
        - session : aiohttp.ClientSession
            - a reference to the aiohttp client session
        - kwargs
            -  keyword parameters to pass to session.get() as params

    Optional Parameters as kwargs:
        - callback : str
            - request data to be returned as a JsonP callback
        - locale : str
            - what locale to use in the response. Default locale is enUS. 
                - Available locales: enUS, enGB, deDE, esES, esMX, frFR, itIT, 
                koKR, plPL, ptBR, ruRU, zhCN, zhTW, jaJP, thTH
    
    Returns:
        the raw response from the endpoint as a JSON
    """
    endpoint = "/info"
    api_result = await _make_request(session, _BASE_URL+endpoint,
                                    _HEADERS, kwargs)
    
    return api_result

@AsyncLRU(maxsize=128) 
async def fetch_cards(session :aiohttp.ClientSession, name :str, 
                      **kwargs) -> Union[
                                    MultipleCards, 
                                    Union[CollectibleCard, NonCollectibleCard]
                                   ]:
    """Make an asynchronous request to /cards/{name} endpoint.

    Positional Arguments:
        - session : aiohttp.ClientSession
            - a reference to the aiohttp client session
        - name : str
            - the full name or dbfid of a hearthstone card
        - kwargs
            -  keyword parameters to pass to session.get() as params

    Optional Parameters as kwargs:
        - callback : str
            - request data to be returned as a JsonP callback
        - collectible : number
            - Set this to 1 to only return collectible cards
        - locale : str
            - what locale to use in the response. Default locale is enUS. 
                - Available locales: enUS, enGB, deDE, esES, esMX, frFR, itIT, 
                koKR, plPL, ptBR, ruRU, zhCN, zhTW, jaJP, thTH

    Raises InvalidArgument when ``if not name`` evaluates to True.

    Returns:
        a MultipleCards, CollectibleCard, or a NonCollectibleCard object. If
        the endpoint failed to return data a NoCardFound exception will be
        raised
    """
    if not name:
        raise InvalidArgument("'name' argument must not be empty or NoneType")
    
    endpoint = f"/cards/{name}"
    api_result = await _make_request(session, _BASE_URL+endpoint,
                                    _HEADERS, kwargs)
    
    return parse_api_result(api_result)

@AsyncLRU(maxsize=128)
async def fetch_cards_by_class(session :aiohttp.ClientSession, hs_class :str, 
                               **kwargs) -> Union[
                                                MultipleCards, 
                                                Union[
                                                    CollectibleCard, 
                                                    NonCollectibleCard
                                                ]
                                            ]:
    """Make an asynchronous request to /cards/classes/{hs_class} endpoint.

    Positional Arguments:
        - session : aiohttp.ClientSession
            - a reference to the aiohttp client session
        - hs_class : str
            - a hearthstone class (E.g: Mage)
        - kwargs
            -  keyword parameters to pass to session.get() as params

    Optional Parameters as kwargs:
        - health : number
            - return only cards with a certain health
        - durability : number
            - return only cards with a certain durability
        - cost : number
            - return only cards of a certain cost
        - attack : number
            - return only cards with a certain attack
        - callback : str
            - request data to be returned as a JsonP callback
        - collectible : number
            - Set this to 1 to only return collectible cards
        - locale : str
            - what locale to use in the response. Default locale is enUS. 
                - Available locales: enUS, enGB, deDE, esES, esMX, frFR, itIT, 
                koKR, plPL, ptBR, ruRU, zhCN, zhTW, jaJP, thTH

    Raises InvalidArgument when ``if not hs_class`` evaluates to True.

    Returns:
        a MultipleCards, CollectibleCard, or a NonCollectibleCard object. If
        the endpoint failed to return data a NoCardFound exception will be
        raised
    """     
    if not hs_class:
        raise InvalidArgument("'hs_class' argument must not be "
                                "empty or NoneType")
    
    endpoint = f"/cards/classes/{hs_class}"  
    api_result = await _make_request(session, _BASE_URL+endpoint,
                                    _HEADERS, kwargs)
    
    return parse_api_result(api_result)

@AsyncLRU(maxsize=128)
async def fetch_cards_by_race(session :aiohttp.ClientSession, race :str, 
                              **kwargs) -> Union[
                                                MultipleCards, 
                                                Union[
                                                    CollectibleCard, 
                                                    NonCollectibleCard
                                                ]
                                           ]:
    """Make an asynchronous request to /cards/races/{race} endpoint.

    Positional Arguments:
        - session : aiohttp.ClientSession
            - a reference to the aiohttp client session
        - race : str
            - a hearthstone race (E.g: Mech)
        - kwargs
            -  keyword parameters to pass to session.get() as params

    Optional Parameters as kwargs:
        - health : number
            - return only cards with a certain health
        - durability : number
            - return only cards with a certain durability
        - cost : number
            - return only cards of a certain cost
        - attack : number
            - return only cards with a certain attack
        - callback : str
            - request data to be returned as a JsonP callback
        - collectible : number
            - Set this to 1 to only return collectible cards
        - locale : str
            - what locale to use in the response. Default locale is enUS. 
                - Available locales: enUS, enGB, deDE, esES, esMX, frFR, itIT, 
                koKR, plPL, ptBR, ruRU, zhCN, zhTW, jaJP, thTH

    Raises InvalidArgument when ``if not race`` evaluates to True.

    Returns:
        a MultipleCards, CollectibleCard, or a NonCollectibleCard object. If
        the endpoint failed to return data a NoCardFound exception will be
        raised
    """           
    if not race:
        raise InvalidArgument("'race' argument must not be "
                                "empty or NoneType")
    
    endpoint = f"/cards/races/{race}"  
    api_result = await _make_request(session, _BASE_URL+endpoint,
                                    _HEADERS, kwargs)
    
    return parse_api_result(api_result)

@AsyncLRU(maxsize=128)
async def fetch_card_set(session :aiohttp.ClientSession, hs_set :str, 
                         **kwargs) -> Union[
                                            MultipleCards, 
                                            Union[
                                                CollectibleCard, 
                                                NonCollectibleCard
                                            ]
                                      ]:
    """Make an asynchronous request to /cards/sets/{hs_set} endpoint.

    Positional Arguments:
        - session : aiohttp.ClientSession
            - a reference to the aiohttp client session
        - hs_set : str
            - a hearthstone set (E.g: Knights of the Frozen Throne)
        - kwargs
            -  keyword parameters to pass to session.get() as params

    Optional Parameters as kwargs:
        - health : number
            - return only cards with a certain health
        - durability : number
            - return only cards with a certain durability
        - cost : number
            - return only cards of a certain cost
        - attack : number
            - return only cards with a certain attack
        - callback : str
            - request data to be returned as a JsonP callback
        - collectible : number
            - Set this to 1 to only return collectible cards
        - locale : str
            - what locale to use in the response. Default locale is enUS. 
                - Available locales: enUS, enGB, deDE, esES, esMX, frFR, itIT, 
                koKR, plPL, ptBR, ruRU, zhCN, zhTW, jaJP, thTH
    
    Raises InvalidArgument when ``if not hs_set`` evaluates to True.

    Returns:
        a MultipleCards, CollectibleCard, or a NonCollectibleCard object. If
        the endpoint failed to return data a NoCardFound exception will be
        raised
    """           
    if not hs_set:
        raise InvalidArgument("'hs_set' argument must not be "
                                "empty or NoneType")
    
    endpoint = f"/cards/sets/{hs_set}"  
    api_result = await _make_request(session, _BASE_URL+endpoint,
                                    _HEADERS, kwargs)
    
    return parse_api_result(api_result)

@AsyncLRU(maxsize=128)
async def fetch_cards_by_quality(session :aiohttp.ClientSession, quality :str, 
                                 **kwargs) -> Union[
                                                MultipleCards, 
                                                Union[
                                                    CollectibleCard, 
                                                    NonCollectibleCard
                                                ]
                                              ]: 
    """Make an asynchronous request to /cards/qualities/{quality} endpoint.

    Positional Arguments:
        - session : aiohttp.ClientSession
            - a reference to the aiohttp client session
        - hs_set : str
            - a hearthstone card quality (E.g: Legendary)
        - kwargs
            -  keyword parameters to pass to session.get() as params

    Optional Parameters as kwargs:
        - health : number
            - return only cards with a certain health
        - durability : number
            - return only cards with a certain durability
        - cost : number
            - return only cards of a certain cost
        - attack : number
            - return only cards with a certain attack
        - callback : str
            - request data to be returned as a JsonP callback
        - collectible : number
            - Set this to 1 to only return collectible cards
        - locale : str
            - what locale to use in the response. Default locale is enUS. 
                - Available locales: enUS, enGB, deDE, esES, esMX, frFR, itIT, 
                koKR, plPL, ptBR, ruRU, zhCN, zhTW, jaJP, thTH
    
    Raises InvalidArgument when ``if not quality`` evaluates to True.

    Returns:
        a MultipleCards, CollectibleCard, or a NonCollectibleCard object. If
        the endpoint failed to return data a NoCardFound exception will be
        raised
    """     
    if not quality:
        raise InvalidArgument("'quality' argument must not be "
                                "empty or NoneType")
    
    endpoint = f"/cards/qualities/{quality}"  
    api_result = await _make_request(session, _BASE_URL+endpoint,
                                    _HEADERS, kwargs) 
    
    return parse_api_result(api_result)

@AsyncLRU(maxsize=4)
async def fetch_cardbacks(session :aiohttp.ClientSession, **kwargs) \
                        -> Union[MultipleCards, Cardback]:
    """Make an asynchronous request to /cardbacks endpoint.

    Positional Arguments:
        - session : aiohttp.ClientSession
            - a reference to the aiohttp client session
        - kwargs
            -  keyword parameters to pass to session.get() as params

    Optional Parameters as kwargs:
        - callback : str
            - request data to be returned as a JsonP callback
        - locale : str
            - what locale to use in the response. Default locale is enUS. 
                - Available locales: enUS, enGB, deDE, esES, esMX, frFR, itIT, 
                koKR, plPL, ptBR, ruRU, zhCN, zhTW, jaJP, thTH
    Returns:
        a MultipleCards or Cardback object. If the endpoint failed to return 
        data a NoCardbackFound exception will be raised
    """       

    endpoint = "/cardsbacks"  
    api_result = await _make_request(session, _BASE_URL+endpoint,
                                    _HEADERS, kwargs)
    
    return parse_cardback_api_result(api_result)

@AsyncLRU(maxsize=128)
async def fetch_card_by_partial_name(session :aiohttp.ClientSession, 
                                     partial_name :str, **kwargs) \
                                     -> Union[
                                            MultipleCards, 
                                            Union[
                                                CollectibleCard, 
                                                NonCollectibleCard
                                            ]
                                        ]:
    """Make an asynchronous request to /cards/search/{partial_name} endpoint.

    Positional Arguments:
        - session : aiohttp.ClientSession
            - a reference to the aiohttp client session
        - partial_name : str
            - a partial name to query (E.g: Reno)
        - kwargs
            -  keyword parameters to pass to session.get() as params

    Optional Parameters as kwargs:
        - callback : str
            - request data to be returned as a JsonP callback
        - collectible : number
            - Set this to 1 to only return collectible cards
        - locale : str
            - what locale to use in the response. Default locale is enUS. 
                - Available locales: enUS, enGB, deDE, esES, esMX, frFR, itIT, 
                koKR, plPL, ptBR, ruRU, zhCN, zhTW, jaJP, thTH

    Raises InvalidArgument when ``if not partial_name`` evaluates to True.

    Returns:
        a MultipleCards, CollectibleCard, or a NonCollectibleCard object. If
        the endpoint failed to return data a NoCardFound exception will be
        raised
    """       
    if not partial_name:
        raise InvalidArgument("'partial_name' argument must not be "
                                "empty or NoneType")
    
    endpoint = f"/cards/search/{partial_name}"  
    api_result = await _make_request(session, _BASE_URL+endpoint,
                                    _HEADERS, kwargs)
    
    return parse_api_result(api_result)

@AsyncLRU(maxsize=128)
async def fetch_cards_by_faction(session :aiohttp.ClientSession, faction :str, 
                                 **kwargs) -> Union[
                                                MultipleCards, 
                                                Union[
                                                    CollectibleCard, 
                                                    NonCollectibleCard
                                                ]
                                              ]:
    """Make an asynchronous request to /cards/factions/{faction} endpoint.

    Positional Arguments:
        - session : aiohttp.ClientSession
            - a reference to the aiohttp client session
        - faction : str
            - a hearthstone faction (E.g: Horde)
        - kwargs
            -  keyword parameters to pass to session.get() as params

    Optional Parameters as kwargs:
        - health : number
            - return only cards with a certain health
        - durability : number
            - return only cards with a certain durability
        - cost : number
            - return only cards of a certain cost
        - attack : number
            - return only cards with a certain attack
        - callback : str
            - request data to be returned as a JsonP callback
        - collectible : number
            - Set this to 1 to only return collectible cards
        - locale : str
            - what locale to use in the response. Default locale is enUS. 
                - Available locales: enUS, enGB, deDE, esES, esMX, frFR, itIT, 
                koKR, plPL, ptBR, ruRU, zhCN, zhTW, jaJP, thTH
    
    Raises InvalidArgument when ``if not faction`` evaluates to True.

    Returns:
        a MultipleCards, CollectibleCard, or a NonCollectibleCard object. If
        the endpoint failed to return data a NoCardFound exception will be
        raised
    """       
    if not faction:
        raise InvalidArgument("'faction' argument must not be "
                                "empty or NoneType")
    
    endpoint = f"/cards/factions/{faction}"  
    api_result = await _make_request(session, _BASE_URL+endpoint,
                                    _HEADERS, kwargs)
    
    return parse_api_result(api_result)

@AsyncLRU(maxsize=128)
async def fetch_cards_by_type(session :aiohttp.ClientSession, card_type :str, 
                              **kwargs) -> Union[
                                            MultipleCards, 
                                            Union[
                                                CollectibleCard, 
                                                NonCollectibleCard
                                            ]
                                           ]:
    """Make an asynchronous request to /cards/types/{card_type} endpoint.

    Positional Arguments:
        - session : aiohttp.ClientSession
            - a reference to the aiohttp client session
        - card_type : str
            - a hearthstone card type (E.g: Spell)
        - kwargs
            -  keyword parameters to pass to session.get() as params

    Optional Parameters as kwargs:
        - health : number
            - return only cards with a certain health
        - durability : number
            - return only cards with a certain durability
        - cost : number
            - return only cards of a certain cost
        - attack : number
            - return only cards with a certain attack
        - callback : str
            - request data to be returned as a JsonP callback
        - collectible : number
            - Set this to 1 to only return collectible cards
        - locale : str
            - what locale to use in the response. Default locale is enUS. 
                - Available locales: enUS, enGB, deDE, esES, esMX, frFR, itIT, 
                koKR, plPL, ptBR, ruRU, zhCN, zhTW, jaJP, thTH

    Raises InvalidArgument when ``if not card_type`` evaluates to True.

    Returns:
        a MultipleCards, CollectibleCard, or a NonCollectibleCard object. If
        the endpoint failed to return data a NoCardFound exception will be
        raised
    """       
    if not card_type:
        raise InvalidArgument("'card_type' argument must not be "
                                "empty or NoneType")
    
    endpoint = f"/cards/types/{card_type}"  
    api_result = await _make_request(session, _BASE_URL+endpoint,
                                    _HEADERS, kwargs)
    
    return parse_api_result(api_result)

@AsyncLRU(maxsize=2)
async def fetch_all_cards(session :aiohttp.ClientSession, **kwargs) \
                            -> Union[
                                    MultipleCards, 
                                    Union[
                                        CollectibleCard, 
                                        NonCollectibleCard
                                    ]
                               ]:
    """Make an asynchronous request to /cards endpoint.

    Positional Arguments:
        - session : aiohttp.ClientSession
            - a reference to the aiohttp client session
        - kwargs
            -  keyword parameters to pass to session.get() as params

    Optional Parameters as kwargs:
        - health : number
            - return only cards with a certain health
        - durability : number
            - return only cards with a certain durability
        - cost : number
            - return only cards of a certain cost
        - attack : number
            - return only cards with a certain attack
        - callback : str
            - request data to be returned as a JsonP callback
        - collectible : number
            - Set this to 1 to only return collectible cards
        - locale : str
            - what locale to use in the response. Default locale is enUS. 
                - Available locales: enUS, enGB, deDE, esES, esMX, frFR, itIT, 
                koKR, plPL, ptBR, ruRU, zhCN, zhTW, jaJP, thTH

    Raises InvalidArgument when ``if not hs_set`` evaluates to True.

    Returns:
        a MultipleCards object. If the endpoint failed to return data a 
        NoCardFound exception will be raised
    """       

    endpoint = "/cards"  
    api_result = await _make_request(session, _BASE_URL+endpoint,
                                    _HEADERS, kwargs)
    
    return parse_api_result(api_result)

import aiohttp
from typing import Any, Coroutine, Union
from cache import AsyncLRU

from .errors import InvalidArgument
from .utils import parse_api_result, parse_cardback_api_result
from ._card import MultipleCards, CollectibleCard, NonCollectibleCard
from ._api import ENV

_BASE_URL = ENV["API_URI"]
_HEADERS =  {
        'x-rapidapi-host': ENV["API_HOST"], 
        'x-rapidapi-key' : ENV["API_KEY"]
} 

async def _make_request(session :aiohttp.ClientSession, 
                        url :str, headers :dict, params :dict) -> Coroutine:
    async with session.get(url=url, headers=headers, params=params) as req:
        response = await req.json()
    return response

@AsyncLRU(maxsize=128)
async def fetch_info(session :aiohttp.ClientSession) -> Any:
    endpoint = "/info"
    api_result = await _make_request(session, _BASE_URL+endpoint,
                                    _HEADERS, None)
    
    return api_result

@AsyncLRU(maxsize=128) 
async def fetch_cards(session :aiohttp.ClientSession, name :str, 
                      **kwargs) -> Union[
                                    MultipleCards, 
                                    Union[CollectibleCard, NonCollectibleCard]
                                   ]:
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
    if not quality:
        raise InvalidArgument("'quality' argument must not be "
                                "empty or NoneType")
    
    endpoint = f"/cards/qualities/{quality}"  
    api_result = await _make_request(session, _BASE_URL+endpoint,
                                    _HEADERS, kwargs) 
    
    return parse_api_result(api_result)

@AsyncLRU(maxsize=4)
async def fetch_cardbacks(session :aiohttp.ClientSession, **kwargs) \
                        -> Union[
                            MultipleCards, 
                            Union[
                                CollectibleCard, 
                                NonCollectibleCard
                            ]
                           ]:      

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
    if not partial_name:
        raise InvalidArgument("'name' argument must not be "
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

    endpoint = "/cards"  
    api_result = await _make_request(session, _BASE_URL+endpoint,
                                    _HEADERS, kwargs)
    
    return parse_api_result(api_result)

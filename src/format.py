from typing import Union
from discord import Embed
from src.hearthstone._card import CollectibleCard, NonCollectibleCard
from src.hearthstone.errors import NoDataFound

def _create_embed(card :Union[CollectibleCard, NonCollectibleCard]) -> Embed:
    """Created a Discord.Embed. For each attr in card create a field
    with name=attr.title() and value=getattr(card, attr). If the value is
    of type list, set value to a ',' separated string of items from value list
    
    Positional Arguments:
        - card : CollectibleCard or NonCollectibleCard
            - a Card object that represents the data of a card fetched from 
            the hearthstone api

    Returns:
        a populated Discord.Embed object

    AttributeError is raised if an exception is found
    """
    try:
        embed = Embed(type="rich")
        for attr in vars(card):
            _name = attr.title()
            _value = getattr(card, attr)
            if isinstance(_value, list):
                _value = ", ".join(_value[i]["name"] 
                                    for i in range(0, len(_value)))
            embed.add_field(name=_name, value=_value, inline=False)
        embed.set_image(url=card.img)
    except AttributeError:
        raise 

    return embed

def format_card(card : Union[CollectibleCard, NonCollectibleCard]) -> str:
    """Return a URL for the card's image
    
    Positional Arguments:
        - card : CollectibleCard or NonCollectibleCard
            - a Card object that represents the data of a card fetched from 
            the hearthstone api

    Returns:
        card.img

    NoDataFound is raised when card.img does not exist 
    """
    try:
        return card.img
    except AttributeError:
        raise NoDataFound(f"No 'img' found for {card}")

def format_card_metadata_embeded(
        card :Union[CollectibleCard, NonCollectibleCard]) -> Embed:
    """Create and return a Discord.Embed if card has all of its attributes
    populated

    Positional Arguments:
        - card : CollectibleCard or NonCollectibleCard
            - a Card object that represents the data of a card fetched from 
            the hearthstone api

    Returns:
        the Discord.Embed object from _create_embed
        
    If an AttributeError is raised from _create_embed, raise NoDataFound
    exception

    If not card, Raise NoDataFound exception
    """
    if card:
        try:
            return _create_embed(card)
        except AttributeError:
            raise NoDataFound(f"Missing Metadata for card: {card}")
    else:
        raise NoDataFound(f"Missing Metadata for card: {card}")
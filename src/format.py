from typing import Union
from discord import Embed
from src.hearthstone._card import CollectibleCard, NonCollectibleCard


class FormattingException(Exception): 
    """Base exception raised when an error occurs while Formatting"""
    pass

class MissingData(FormattingException):
    """Exception that is raised when an expected attribute of a concrete
    implemented _Card object is missing
    """
    pass

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

    Raised a FormattingException if an attribute is not found
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
    except AttributeError as e:
        raise FormattingException(e)

    return embed

def format_card(card : Union[CollectibleCard, NonCollectibleCard]) -> str:
    """Return a URL for the card's image
    
    Positional Arguments:
        - card : CollectibleCard or NonCollectibleCard
            - a Card object that represents the data of a card fetched from 
            the hearthstone api

    Returns:
        card.img

    Raises a FormattingException when card.img does not exist 
    """
    try:
        return card.img
    except AttributeError:
        raise FormattingException(f"No 'img' found for {card}")

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

    Raises a MissingData exception when `if card` evaluates to False
    """
    if card:
        return _create_embed(card)
    else:
        raise MissingData(f"Missing Metadata for card: {card}")
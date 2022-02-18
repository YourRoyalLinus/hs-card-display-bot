from typing import Union
from discord import Embed
from src.hearthstone._card import CollectibleCard, NonCollectibleCard
from src.hearthstone.errors import NoDataFound

def _create_embed(card :Union[CollectibleCard, NonCollectibleCard]) -> Embed:
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
    try:
        return card.img
    except AttributeError:
        raise NoDataFound(f"No 'img' found for {card}")

def format_card_metadata_embeded(
        card :Union[CollectibleCard, NonCollectibleCard]) -> Embed:
    if card:
        try:
            return _create_embed(card)
        except AttributeError:
            raise NoDataFound(f"Missing Metadata for card: {card}")
    else:
        raise NoDataFound(f"Missing Metadata for card: {card}")
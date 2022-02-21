__all__ = (
    "CollectibleCard", 
    "NonCollectibleCard", 
    "MultipleCards"
)

import operator
from abc import ABCMeta
from typing import Union
from functools import reduce
from .errors import NoCardFound 

class _Card(metaclass=ABCMeta):
    """An abstract class that represents a Card returned by the hearthstone
    api
    """
    def __init__(self, dict: dict):
        self.__dict__ = dict

    def __repr__(self) -> str:
        cls = type(self).__name__
        return "{}({})".format(cls, self.__dict__)

    def __str__(self) -> str:
        """Return the 'name' attribute, if that doesn't exist, the card is
        considered an 'Invalid Card'
        """
        try:
            name = getattr(self, 'name')
        except AttributeError:
            return "Invalid Card"

        cls = type(self).__name__
        return cls + ": " + name

    def __bool__(self) -> bool:
        """Return True if all values in _Card.__dict__ are truthy"""
        if all(value for value in self.__dict__.values()):
            return True
        else:
            return False

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, _Card):
            return (self.__dict__ == __o.__dict__)
        else:
            return False

    def __hash__(self) -> int:
        return reduce(hash, self.__dict__.values(), 0)

class CollectibleCard(_Card):
    """A concrete class that subclasses _Card and represents a collectible 
    card returned by the hearthstone api. All CollectibleCards have a 
    'collectible' attribute equal to 1 or a truthy value
    """
    def __init__(self, dict: dict):
        super().__init__(dict)

class NonCollectibleCard(_Card):
    """A concrete class that subclasses _Card and represents a non-collectible 
    card returned by the hearthstone api.
    """
    def __init__(self, dict: dict):
        super().__init__(dict)
        
class Cardback(_Card):
    """A concrete class that subclasses _Card and represents a cardback
    returned by the hearthstone api.
    """
    def __init__(self, dict: dict):
        super().__init__(dict)

class MultipleCards:
    """
    A data structure that represents multiple _Card objects returned by the
    hearthstone API. This will typically occur when a user makes a query using
    partial name search.
    """
    def __init__(self, cards: list):
        self._cards = [card for card in cards]
    
    def __iter__(self):
        return iter(self._cards)

    def __len__(self):
        return len(self._cards)
    
    def __getitem__(self, index):
        """Given an index, if it a string, iterate through the underlying 
        sequence of cards and attempt to match index to card.name. If no
        such card exists such that card[i]['name'] == index raise NoCardFound.
        If such a card does exist, call _find_card_type and pass it the card
        metadata from self.

        If the index is not a string, attempt to return sequence[index]
        """
        if isinstance(index, str):
            for i in range(0, len(self)):
                if self._cards[i]["name"] == index:
                    return _find_card_type(self._cards[i])
            raise NoCardFound("No card with name '{index}' found")
        else:
            return self._cards[index]

    def __repr__(self) -> str:
        cls = type(self).__name__
        return "{}({})".format(cls, self.__dict__)

    def __str__(self) -> str:
        cls = type(self).__name__ +f" [{len(self)}]: "
        return cls + ", ".join([card["cardId"] for card in self._cards])

    def __bool__(self):
        """Return True if the number of cards in the underlying sequence is
        greater than 1
        """
        return (self._cards > 1)
    
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, MultipleCards):
            if len(__o) == len(self):
                for i in range(0, len(__o)):
                    if __o[i] != self[i]:
                        return False
                return True
            else:
                return False
        else:
            return False

    def __hash__(self) -> int:
        hashes = (hash(i) for i in self)
        return reduce(operator.xor, hashes, 0)
                    
def _find_card_type(card_metadata :dict) -> Union[
                                                Cardback,
                                                Union[
                                                    CollectibleCard,
                                                    NonCollectibleCard
                                                ]
                                            ]:
    """Inspect the keys of card_metadata and return a new instance
    of a concrete _Card implementation that corresponds to the suspected card 
    type. 

    Positional Arguments:
        - card_metadata : dict
            - a dictionary object that contains the card metadata

    Returns:
        a concrete _Card implemented class inferred from the keys of 
        card_metadata
    """
    if("cardBackId" in card_metadata.keys()):
        return Cardback(card_metadata)
    elif ("collectible" in card_metadata.keys() and 
        card_metadata["collectible"]):
        return CollectibleCard(card_metadata)
    else:
        return NonCollectibleCard(card_metadata)


    


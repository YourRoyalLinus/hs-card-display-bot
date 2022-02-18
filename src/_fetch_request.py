import operator
from abc import ABCMeta
from typing import Callable, Set, List
from functools import reduce
from src.hearthstone.hearthstone import fetch_card_by_partial_name
from src.format import format_card, format_card_metadata_embeded

class _FetchRequest(metaclass=ABCMeta):
    """An abstract class that represents a FetchRequest generated by a user 
    and to be handled by the bot
    
    Attributes:
        - items (property) : Set[str]
            - set of args that will be be iterated upon and each item passed to
             _FetchRequest.API
        - API
            - callable that makes a request to the hearthstone api
        - format
            - callable that formats the response from the hearthstone api
            to be displayed by the bot 
    """
    def __init__(self, request_str: List[str]) -> None:
        self.items = request_str

    def __repr__(self) -> str:
        cls = type(self).__name__
        api_fn = self.API.__name__
        fmt_fn = self.format.__name__
        return "{}(API_FN: {}, FORMAT_FN: {}, ITEMS: {})" \
                .format(cls, api_fn, fmt_fn, self.items)
    
    def __str__(self) -> str:
        cls = type(self).__name__
        return cls
    
    def __bool__(self) -> bool:
        return (self.API and self.format and self.items)

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, _FetchRequest):
            return (self.API == __o.API and self.format == __o.format and
                        self.items == __o.items)
        else:
            return False

    def __hash__(self) -> int:
        hashes = (hash(i) for i in self.__dict__)
        return reduce(operator.xor, hashes, 0)

    @property
    def items(self) -> Set[str]:
        """Getter for the items property"""
        return self._items

    @items.setter
    def items(self, value :List[str]) -> None:
        """Setter for the items property that accepts a list of strings and
        creates a set of stripped, titled strings for each string in
        string_element.split('|') for each string_element in value
        """
        self._items = {card.strip().title() for cards in value
                                            for card in cards.split('|')}

    @property
    def API(self) -> Callable:
        """Getter for the API property"""
        return self._api
    
    @property
    def format(self) -> Callable:
        """Getter for the format property"""
        return self._format

class CardFetchRequest(_FetchRequest):
    """A subclass of _FetchRequest that will fetch and format a card's 
    image URL

    Attributes:
        - items (inherited from _FetchRequest) : Set[str]
            - set of args that will be be iterated upon and each item passed to
             _FetchRequest.API
        - API 
            - a callable that makes a request to the hearthstone api
            - set to =hearthstone.fetch_card_by_partial_name
        - format
            - a callable that formats the response from the hearthstone api
            to be displayed by the bot 
            - set to =format.format_card
    """
    def __init__(self, request_str: List[str]) -> None:
        super().__init__(request_str)
        self._api = fetch_card_by_partial_name
        self._format = format_card

class MetadataFetchRequest(_FetchRequest):
    """A subclass of _FetchRequest that will fetch and format a 
    Discord.Embed of the card's metadata

    Attributes:
        - items (inherited from _FetchRequest) : Set[str]
            - set of args that will be be iterated upon and each item passed to
             _FetchRequest.API
        - API 
            - a callable that makes a request to the hearthstone api
            - set to =hearthstone.fetch_card_by_partial_name
        - format
            - a callable that formats the response from the hearthstone api
            to be displayed by the bot 
            - set to =format_card_metadata_embeded
    """
    def __init__(self, request_str: List[str]) -> None:
        super().__init__(request_str)
        self._api = fetch_card_by_partial_name
        self._format = format_card_metadata_embeded
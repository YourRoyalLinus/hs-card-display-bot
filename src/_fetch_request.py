import operator
from typing import Callable
from functools import reduce
from hearthstone.hearthstone import fetch_card_by_partial_name, fetch_cardbacks
from format import format_card, format_card_metadata_embeded, format_cardback

class _FetchRequest:
    def __init__(self, request_str) -> None:
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
    def items(self) -> str:
        return self._items

    @items.setter
    def items(self, value) -> None:
        self._items = {card.strip().title() for cards in value
                                            for card in cards.split('|')}

    @property
    def API(self) -> Callable:
        return self._api
    
    @property
    def format(self) -> Callable:
        return self._format

class CardFetchRequest(_FetchRequest):
    def __init__(self, request_string) -> None:
        super().__init__(request_string)
        self._api = fetch_card_by_partial_name
        self._format = format_card

class CardbackFetchRequest(_FetchRequest):
    def __init__(self, request_string) -> None:
        super().__init__(request_string)
        self._api = fetch_cardbacks
        self._format = format_cardback

class MetadataFetchRequest(_FetchRequest):
    def __init__(self, request_string) -> None:
        super().__init__(request_string)
        self._api = fetch_card_by_partial_name
        self._format = format_card_metadata_embeded
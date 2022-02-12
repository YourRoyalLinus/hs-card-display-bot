from abc import ABCMeta
from ast import operator
from functools import reduce
from .errors import NoCardFound 

class _Card(metaclass=ABCMeta):
    def __init__(self, dict: dict):
        self.__dict__ = dict

    def __repr__(self) -> str:
        cls = type(self).__name__
        return "{}({})".format(cls, self.__dict__)

    def __str__(self) -> str:
        try:
            name = getattr(self, 'name')
        except AttributeError:
            return "Invalid Card"

        cls = type(self).__name__
        return cls + ": " + name

    def __bool__(self) -> bool:
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
    def __init__(self, dict: dict):
        super().__init__(dict)

class NonCollectibleCard(_Card):
    def __init__(self, dict: dict):
        super().__init__(dict)
        
class Cardback(_Card):
    def __init__(self, dict: dict):
        super().__init__(dict)

class MultipleCards: #Handling multiple cards - display or ask to filter?
    def __init__(self, cards: list):
        self._cards = [card for card in cards]
    
    def __iter__(self):
        return iter(self._cards)

    def __len__(self):
        return len(self._cards)
    
    def __getitem__(self, index):
        if isinstance(index, str):
            for i in range(0, len(self)):
                if self._cards[i]["name"] == index: #return CollectibleCard or NonCollectibleCard
                    return self._cards[i]
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
        return (self._cards > 0)
    
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
                    


    


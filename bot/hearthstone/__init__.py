"""A basic wrapper for the Hearthstone API: 
https://rapidapi.com/omgvamp/api/hearthstone/
"""

all = [
    "hearthstone", 
    "errors", 
    "_card",
]

from .hearthstone import *
from .errors import *
from ._card import *




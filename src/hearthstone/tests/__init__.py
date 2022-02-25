"""Test package for the hearthstone api wrapper

Modules
---
    - test_api: tests related to the API server and making API requests
    -test_card_obj: tests related to functionality of the _Card objects 

"""

all = (
    "API_TEST_SUITE",
    "CARD_TEST_SUITE"
)

from .test_api import API_TEST_SUITE
from .test_cards import CARD_TEST_SUITE

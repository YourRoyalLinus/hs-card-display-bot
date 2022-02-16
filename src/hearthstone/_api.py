
"""Module that loads environment variables for the Hearthstone API

GLOBALS:
    ENV : Dict
        API_URI - Base URL for the Hearthstone API
        API_KEY - Key included in headers of requests to Hearthstone API
        API_HOST - Host URL included in headers of requests to Hearthstone API
"""

all = ['ENV']

import os
from dotenv import load_dotenv

load_dotenv()

ENV = {
    "API_URI" : "https://omgvamp-hearthstone-v1.p.rapidapi.com",
    "API_KEY" : os.getenv('RAPID_API_KEY'),
    "API_HOST" : os.getenv('RAPID_API_HOST')
}




"""Module that loads environment variables for the Hearthstone API

GLOBALS:
    ENV : Dict
        API_URI - Base URL for the Hearthstone API
        API_KEY - Key included in headers of requests to Hearthstone API
        API_HOST - Host URL included in headers of requests to Hearthstone API

    A .env file must exist in the root of /hearthstone containing the 
    RAPID_API_KEY and RAPID_API_HOST variables. Users should go to
    'https://rapidapi.com/omgvamp/api/hearthstone/' and register to recieve
    these values.
"""

all = ['ENV']

from os import environ, path
from dotenv import load_dotenv
from pathlib import Path
from .errors import APIException

_env_file_path = str(Path(__file__).parent.resolve()) + "\.env"
if not path.exists(_env_file_path):
    raise APIException("Could not find .env file for hearthstone API. A "
                        ".env file with 'RAPID_API_KEY', 'RAPID_API_HOST' in "
                        " the root of the hearthstone package is missing.")
else:
    load_dotenv(dotenv_path=_env_file_path)

try:
    ENV = {
        "API_URI" : "https://omgvamp-hearthstone-v1.p.rapidapi.com",
        "API_KEY" : environ["RAPID_API_KEY"],
        "API_HOST" : environ["RAPID_API_HOST"],
    }
except KeyError as e:
    raise APIException(f"{e} required but not found in .env")





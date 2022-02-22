import aiohttp
import uuid
from cachetools import Cache, TTLCache
from typing import Any, List, Union
from discord import Embed, Message
from discord import DiscordException
from discord.ext import commands

from .log import get_logger
from ._fetch_request import CardFetchRequest, MetadataFetchRequest
from .message_parser import ParserException, is_valid_request_str
from .message_parser import parse_message
from .format import FormattingException
from .hearthstone import CollectibleCard, NonCollectibleCard, MultipleCards 
from .hearthstone import APIException

logger = get_logger()

class StartUpError(Exception):
    """Exception that is raised when a process required for the bot to function
    fails on creation or initialization
    """
    def __init__(self, base: Exception):
        super().__init__()
        self.exception = base

def _get_bot_token():
    """Return os.getenv["TOKEN"]
    
    .env file searched for in the immediate parent directory of bot.py
    """
    from dotenv import load_dotenv
    from os import getenv
    from pathlib import Path

    env_file_path = str(Path(__file__).parent.resolve()) + "\.env"
    load_dotenv(dotenv_path=env_file_path)

    return getenv("TOKEN")

def _handle_api_results(cache :Cache, result: Any, item :str,
                        request: Union[CardFetchRequest, 
                                            MetadataFetchRequest], 
                        request_id :str) -> dict:
    """Check if the result is of type MultipleCards or not and
    call the proper functions to handle the request accordingly
    
    Positional Arguments:
        - cache : Cache
            - reference to the cache of the bot instance

        - result : Any
            - the object returned by the hearthstone api. A proper response
            will be either MultipleCards, CollectibleCard, or 
            NonCollectibleCard

        - item : str
            - the arguments the request object passed to its API function
            
        - request : CardFetchRequest | MetadataFetchRequest
            - an object that represents the type of request made by the user

        - request_id : str
            - the string representation of the uuid that denotes a valid
            request made by a user and being handled by the bot

    Returns:
        Result of _handle_multiple_cards or _handle_single_card depending on
        the type of result. Both handle functions return a dict object to be
        passed back to bot._handle_requests
    """
    if type(result) is MultipleCards:
        return _handle_multiple_cards(cache, result, item, request_id)             
    else:
        return _handle_single_card(result, item, request, request_id)

def _handle_multiple_cards(cache :Cache,
                            result: MultipleCards, 
                            item :str,
                            request_id :str) -> dict:
    """Iterate through each card and create a list of card name: card database
    file id to be displayed to the user. As we're iterating through the cards
    we will be caching them by their dbfid because card names are NOT UNIQUE.
    By caching and displaying dbfid, we allow a user to make a new request with 
    the dbfid and return the card. This only works if the values were cached 
    first

    Positional Arguments:
        - cache : Cache
            - reference to the cache of the bot instance

        - result : Any
            - the object returned by the hearthstone api guaranteed to be
            type MultipleCards

        - item : str
            - the arguments the request object passed to its API function

        - request_id : str
            - the string representation of the uuid that denotes a valid
            request made by a user and being handled by the bot
    
    Returns:
        dict with one key 'content' whose value is the message to display
        back to the user
    """
    logger.info(f"{request_id} Multiple results for "
                f"'{item}'")
    for card in result:
        cache[card["dbfId"]] = result[card["name"]]

    multiple_results = "\n".join([result[i]['name']
                                    +": "+result[i]['dbfId']
                                    for i in range(0, len(result))])
    return {"content": f"Found more than one result for "
                        f"'{item}': \n{multiple_results}"}
                            
def _handle_single_card(result: Union[CollectibleCard, 
                                NonCollectibleCard], 
                        item :str,
                        request :Union[CardFetchRequest, 
                                MetadataFetchRequest],                     
                        request_id: str) -> dict:
    """Call request.format(result) to format the result of the API call and 
    store the result in the local response variable

    Positional Arguments:
        - result : CollectibleCard | NonCollectibleCard
            - the object returned by the hearthstone api guaranteed to be
            type CollectibleCard or NonCollectibleCard

        - item : str
            - the arguments the request object passed to its API function

        - request : CardFetchRequest | MetadataFetchRequest
            - an object that represents the type of request made by the user

        - request_id : str
            - the string representation of the uuid that denotes a valid
            request made by a user and being handled by the bot
    
    Returns:
        dict with one key 'content' whose value is response. If response is a
        Discord.Embed object, then return a dict with one key 'embed' whose
        value is response
    """
    logger.info(f"{request_id} Fetch successful for "
                f"{type(result).__name__}: {item}")
    
    response = request.format(result)

    if type(response) is Embed:
        return {"embed":response}
    else:
        return {"content":response}
    
class Bot(commands.Bot): 
    """A class that wraps Discord.commands.Bot with an aiohttp session and 
    TTLCache

    Attributes
        - http_session : aiohttp.ClientSession
            - the aiohttp session for the bot instance
        - cache : Cache
            - the ttlcache that stores card_dbfids as keys and CollectibleCard
            or NonCollectibleCards as values
            - max size of 128 and ttl of 10 minutes
        - token (property): str
            - the token needed to authenticate the discord bot
    
    Methods:
        - create (class method)
            - creates an instance of the Bot
        - initialize
            - initializes the http_session, cache, and fetches the token
        - close
            - call close on the parent Bot and close the http_session on the 
            child bot
        - on_ready (event)
            - log that the bot is ready to handle requests
        - on_message (event) 
            - parse messages sent in the discord server and handle any 
            FetchRequests
        - _handle_requests (private)
            - handle the list of FetchRequests generated from parsing the
            discord message
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
    
        self.http_session :aiohttp.ClientSession = None
        self.cache :Cache = None
        self.token :str = None
    
    @classmethod
    def create(cls, *args, **kwargs) -> "Bot":
        """Create and return an instance of Bot
        
        Any exception is raised as a StartUpError
        """
        try:
            return cls(*args, **kwargs)
        except Exception as e:
            raise StartUpError(e)

    def initialize(self) -> None:
        """Initialize the aiohttp client session and cache of the bot and fetch
        its token
        
        Any exception is raised as a StartUpError 
        """
        try:
            self.http_session = aiohttp.ClientSession()
            self.cache =  TTLCache(maxsize=128, ttl=600)
            self._token = _get_bot_token()
        except Exception as e:
            raise StartUpError(e)

        logger.info("Bot initialized successfully!")

    @property
    def token(self) -> str:
        """Getter for the token property that allows the token to be read
        only once before being cleared
        """
        ephemeral_token = ""
        if self._token:
            ephemeral_token = self._token
            self._token = ""

        return ephemeral_token

    @token.setter
    def token(self, value) -> None:
        """Setter for the token property"""
        self._token = value
    
    async def close(self) -> None:
        """Close the Discord connection and aiohttp session"""
        logger.warning("Request to close bot recieved...")
        await super().close()

        if self.http_session:
            await self.http_session.close()
    

    async def on_ready(self) -> None:
        """Event that logs the bot.user.name and bot.user.id when the bot 
        client is done preparing the data received from Discord
        """
        logger.info('Logging in USER: ' + self.user.name 
                + ' ID: ' + str(self.user.id))

    async def on_message(self, message: Message) -> None:
        """Event responds to a Discord.Message being created and sent
        
        if the message is found to be a valid fetch request to be handled by
        the bot, a request_id will be generated and the message will be parsed.
        When the message is parsed, a FetchRequest Object will be created for
        each valid fetch request found in message. These objects have as 
        attributes: the proper API call, formatting callable and a
        set of strings that represent values to be sent to the
        API. The list of FetchRequest objects is then passed to 
        bot._handle_requests to be handled

        Positional Arguments:
            - message : Discord.Message
                - Message object that represents a message sent in a discord 
                server

            - request : CardFetchRequest | MetadataFetchRequest
                - an object that represents the type of request made by the 
                user

            - request_id : str
                - the string representation of the uuid that denotes a valid
                request made by a user and being handled by the bot

        Any Discord.Excpetion raised is logged and calls bot.close()
        """
        if message.author == self.user:
            return
        try: 
            request_id = str(uuid.uuid1())       
            if is_valid_request_str(message.content):        
                logger.info(f"{request_id} Fetch message recieved: "
                            f"{message.content}")
                try:
                    fetch_requests = parse_message(message)
                except ParserException as e:
                    logger.warning(request_id + " " + e.exception + " raised")
                    return

                await self._handle_requests(message, 
                                            fetch_requests, request_id)    
        except DiscordException as e:
            logger.error(request_id + " " + repr(e))
            self.close()
    
    async def _handle_requests(self, message :Message, 
                                requests :List[Union[CardFetchRequest, 
                                                    MetadataFetchRequest]],
                                request_id :str) -> None:
        """Handle the list of FetchRequest objects created when parsing the 
        Discord Message by calling request.API and passing the item for each
        item in requests.items 

        Positional Arguments:
            -  message: Discord.Message:
                - Message object that represents a message sent in a discord 
                server

            - request : List[CardFetchRequest | MetadataFetchRequest]
                - a list of objects that represent the type of request made by
                the user

            - request_id : str
                - the string representation of the uuid that denotes a valid
                request made by a user and being handled by the bot

        The response of _handle_api_results for each request is then passed to
        message.channel.send(**response) to send the response to the channel
        from which the message is called
        """
        for request in requests:
            logger.info(f'{request_id} Executing request: {request}')
            for item in request.items:
                result = self.cache.get(item, None)
                if not result:
                    logger.info(f'{request_id} Fetching {item}')
                    try: 
                        result = await request.API(self.http_session, item)
                    except APIException as e:
                        logger.warning(request_id + " " + repr(e) + " raised")
                        continue
                try:
                    response = _handle_api_results(self.cache, result, item,
                                                    request, request_id)
                except FormattingException as e:
                    logger.warning(request_id + " " + repr(e) + " raised")
                    response = {"content" : e}

                await message.channel.send(**response)

       
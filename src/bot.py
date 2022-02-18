import aiohttp
import uuid
from cachetools import Cache, TTLCache
from typing import Any, List, Union
from discord import Embed, Message
from discord import DiscordException
from discord.ext import commands
from .log import get_logger
from ._fetch_request import CardFetchRequest, MetadataFetchRequest
from .message_parser import is_valid_request_str, parse_message, ParserError
from .hearthstone import CollectibleCard, NonCollectibleCard, MultipleCards 
from .hearthstone import NoCardFound, NoDataFound

logger = get_logger()

class StartUpError(Exception):
    def __init__(self, base: Exception):
        super().__init__()
        self.exception = base

def _get_bot_token():
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
    if type(result) is MultipleCards:
        return _handle_multiple_cards(cache, result, item, request_id)             
    else:
        return _handle_single_card(result, item, request, request_id)

def _handle_multiple_cards(cache :Cache,
                            result: Any, 
                            item :str,
                            request_id :str) -> dict:
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
    logger.info(f"{request_id} Fetch successful for "
                f"{type(result).__name__}: {item}")
    
    response = request.format(result)

    if type(response) is Embed:
        return {"embed":response}
    else:
        return {"content":response}
    
class Bot(commands.Bot): 
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
    
        self.http_session :aiohttp.ClientSession = None
        self.cache :Cache = None
        self.token :str = None
    
    @classmethod
    def create(cls) -> "Bot":
        try:
            return cls(command_prefix='!')
        except Exception as e:
            raise StartUpError(e)

    def initialize(self) -> None:
        try:
            self.http_session = aiohttp.ClientSession()
            self.cache =  TTLCache(maxsize=128, ttl=600)
            self._token = _get_bot_token()
        except Exception as e:
            raise StartUpError(e)

        logger.info("Bot initialized successfully")

    @property
    def token(self) -> str:
        ephemeral_token = ""
        if self._token:
            ephemeral_token = self._token
            self._token = ""

        return ephemeral_token

    @token.setter
    def token(self, value) -> None:
        self._token = value
    
    async def close(self) -> None:
        logger.warning("Closing bot...")
        await super().close()

        if self.http_session:
            await self.http_session.close()
    

    async def on_ready(self) -> None:
        logger.info('Logging in USER: ' + self.user.name 
                + ' ID: ' + str(self.user.id))

    async def on_message(self, message: Message) -> None:
        if message.author == self.user:
            return
        try: 
            request_id = str(uuid.uuid1())       
            if is_valid_request_str(message.content):        
                logger.info(f"{request_id} Fetch message recieved: "
                            f"{message.content}")
                try:
                    fetch_requests = parse_message(message)
                except ParserError as e:
                    logger.warning(request_id + " " + repr(e) + " raised")
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
        for request in requests:
            logger.info(f'{request_id} Executing request: {request}')
            for item in request.items:
                result = self.cache.get(item, None)
                if not result:
                    logger.info(f'{request_id} Fetching {item}')
                    try: 
                        result = await request.API(self.http_session, item)
                    except NoCardFound as e:
                        logger.warning(request_id + " " + repr(e) + " raised")
                        continue
                try:
                    response = _handle_api_results(self.cache, result, item,
                                                    request, request_id)
                except NoDataFound as e:
                    logger.warning(request_id + " " + repr(e) + " raised")
                    response = {"content" : e}

                await message.channel.send(**response)

       
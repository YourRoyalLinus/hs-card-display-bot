import sys
import aiohttp
import uuid
from  cachetools import TTLCache
import discord
from discord.ext import commands
from log import get_logger
from message_parser import is_valid_request_str, parse_message, ParserError
from hearthstone import MultipleCards, NoCardFound, NoDataFound

#temporary
import os
from dotenv import load_dotenv

load_dotenv()
_TOKEN = os.getenv("TOKEN")

this = sys.modules[__name__]

bot = commands.Bot(command_prefix='!')
cache = TTLCache(maxsize=128, ttl=600)
logger = get_logger()

@bot.event
async def on_ready():
    this.session = aiohttp.ClientSession()
    logger.info('Logging in USER: ' + bot.user.name 
                + ' ID: ' + str(bot.user.id))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    try: 
        request_id = str(uuid.uuid1())
        
        if is_valid_request_str(message.content):        
            logger.info(f"{request_id} Fetch message recieved: "
                        f"{message.content}")

            try:
                fetch_requests = parse_message(message)
            except ParserError as e:
                logger.warning(request_id + " " + repr(e))
                return

            for request in fetch_requests:
                logger.info(f'{request_id} Executing request: {request}')

                for item in request.items:
                    result = cache.get(item, None)
                    if not result:
                        logger.info(f'{request_id} Fetching {item}')
                        try: 
                            result = await request.API(this.session, item)
                        except NoCardFound as e:
                            logger.warning(request_id + " " + repr(e))
                            continue

                    if type(result) is MultipleCards:
                        logger.warning(f"{request_id} Multiple results for "
                                       f"'{item}'")
                        for card in result:
                            cache[card["dbfId"]] = result[card["name"]]
                        multiple_results = "\n".join([result[i]['name']
                                                     +": "+result[i]['dbfId']
                                                    for i in 
                                                        range(0, len(result))])
                        await message.channel.send(f"Found more "
                                                    "than one result for "
                                                    f"'{item}': \n"
                                                    f"{multiple_results}")                      
                    else:
                        logger.info(
                            f"{request_id} Fetch successful for "
                                    f"{type(result).__name__}: {item}")
                        try:
                            response = request.format(result)
                        except NoDataFound as e:
                            logger.warning(request_id + " " + repr(e))

                        if type(response) is discord.Embed:
                            try:
                                await message.channel.send(embed=response)
                            except NoDataFound as e:
                                logger.warning(request_id + " " + repr(e))
                        else:
                            try:
                                await message.channel.send(response)
                            except NoDataFound as e:
                                logger.warning(request_id + " " + repr(e))
        else:
            logger.warning(f"{request_id} Non-Request Message: " #Do we wanna log every msg????
                                            f"{message.content}")
    except discord.DiscordException as e:
        logger.error(request_id + " " + repr(e))

bot.run(_TOKEN)
this.session.close()

"""
TODO
organize bot.py into smaller functions (decide where those go)
    - WRITE FUNCTION TO FETCH CARDS FROM DATABASE (Figure out exactly how I wanna do this, collectible vs non, show stats, include BG heros?, show golden img)
    - WRITE JSON PARSER FOR CARD METADATA (make hashable for LRU caching)
    - IMPROVE ERROR HANDLING
    - LOGGING DECORATOR
    - CACHING
    - ASYNC/MULTITHREADING
    - OPTIMIZATION
    - PROPER PROJECT STRUCTURING
    [](){}
    Bot commands to change settings
     - [] be golden by default
"""
import sys
import aiohttp
import discord
from discord.ext import commands

from log import get_logger
from env.env import _ENV #package
from hearthstone.hearthstone import fetch_card_by_partial_name #NEED2TEST ALL FUNCTIONS (FUNCTIONALLY + NON FUNCTIONALLY)
from hearthstone._card import MultipleCards
from hearthstone.errors import NoCardFound

this = sys.modules[__name__]

bot = commands.Bot(command_prefix='!')
logger = get_logger()

@bot.event
async def on_ready():
    session_headers = {
        'x-rapidapi-host': _ENV["API_HOST"], 
        'x-rapidapi-key' : _ENV["API_KEY"]
    } 
    this.session = aiohttp.ClientSession(headers=session_headers)
    logger.info('Logging in USER: ' + bot.user.name 
                + ' ID: ' + str(bot.user.id))

@bot.event #Refactor using commands + enhanced error handling
async def on_message(message):
    if message.author == bot.user:
        return
    try:
        is_fetch_command = False 
        if message.content[0] == '[' and message.content[-1] == ']':  #Smarter checks for this to have "Hey I think [CARD] is op" work
            is_fetch_command = True
            logger.info(f'Fetch command recieved: {message.content}')

        if is_fetch_command:
            card_names = message.content.replace('[', '').replace(']', '')
            cards = {card.strip().title() for card in card_names.split('|')}
            for card in cards:
                logger.info(f'Fetching {card}')
                try:
                    result = await fetch_card_by_partial_name(this.session, card)
                except NoCardFound as e:
                    await message.channel.send(f'No card found with name: {card}')
                    logger.warning(repr(e))
                    return
                    
                if type(result) is MultipleCards: #May need to become a raised exception, depends on how I wanna handle
                    multiple_results = " | ".join({"**"+result[i]['name']+"**" for i in range(0, len(result))})
                    logger.warning(f'Multiple results for {card}')
                    await message.channel.send(f'Found more than one result for {card}: {multiple_results}') 
                else:
                    logger.info(f'Fetch successful for {type(card).__name__}: {card}')
                    await message.channel.send(result.img) #handle img empty?
    except discord.DiscordException as e:
        logger.error(str(e))

bot.run(_ENV["TOKEN"])
this.session.close()

"""
TODO
    - WRITE FUNCTION TO FETCH CARDS FROM DATABASE (Figure out exactly how I wanna do this, collectible vs non, show stats, include BG heros?, show golden img)
    - WRITE JSON PARSER FOR CARD METADATA (make hashable for LRU caching)
    - IMPROVE ERROR HANDLING
    - LOGGING DECORATOR
    - CACHING
    - ASYNC/MULTITHREADING
    - OPTIMIZATION

    [](){}
    Bot commands to change settings
     - [] be golden by default
"""
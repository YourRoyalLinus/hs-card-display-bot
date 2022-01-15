import os, requests, discord, json, logging, datetime
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
API_URI = "https://omgvamp-hearthstone-v1.p.rapidapi.com/cards/search/"
API_KEY = os.getenv('RAPID_API_KEY')
API_HOST = os.getenv('RAPID_API_HOST')

bot = commands.Bot(command_prefix='!')

LOGGING_DIR = r'./logs/'
LOGGING_DATE = datetime.datetime.today().strftime('%Y%m%d')
LOG_FILE = LOGGING_DIR + 'LOG_' + LOGGING_DATE + '.log'

def fetch_card(card_name :str):
    headers = {'x-rapidapi-host': API_HOST, 'x-rapidapi-key' : API_KEY}
    params = {'collectible' : 1}
    url = API_URI + card_name
    r = requests.get(url=url, headers=headers, params=params)
    return r.json()

@bot.event
async def on_ready():
    print(datetime.datetime.today().strftime('%m/%d/%Y %H:%M:%S') + ' Logging in -> %s USER: ' + bot.user.name + ' ID: ' + str(bot.user.id))
    logging.FileHandler(LOG_FILE, mode='a', encoding='utf-8')
    logging.basicConfig(filename=LOG_FILE, filemode='a', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %H:%M:%S')
    logging.info('Logging in USER: ' + bot.user.name + ' ID: ' + str(bot.user.id))

@bot.event #Refactor using commands + enhanced error handling
async def on_message(message):
    if message.author == bot.user:
        return

    try:
        is_fetch_command = False 
        if message.content[0] == '[' and message.content[-1] == ']':  #Smarter checks for this to have "Hey I think [CARD] is op" work
            is_fetch_command = True
            logging.info(f'Fetch command recieved: {message.content}')
        
        if is_fetch_command:
            card_names = message.content.replace('[', '').replace(']', '')
            cards = {card.strip().title() for card in card_names.split('|')}
            for card in cards:
                logging.info(f'Fetching {card}')
                result = fetch_card(card)
                if type(result) is dict and result.get('error') is not None:
                    logging.warning(f'No card found with name: {card}')
                    await message.channel.send(f'No card found with name: {card}')
                elif len(result) > 1:
                    multiple_results = " | ".join({"**"+result[i]['name']+"**" for i in range(0, len(result))})
                    logging.warning(f'Multiple results for {card}')
                    await message.channel.send(f'Found more than one result for {card}: {multiple_results}')
                else:
                    logging.info(f'Fetch successful for {card}')
                    await message.channel.send(result[0]['img']) #handle img empty?
    except discord.DiscordException as e:
        logging.error(str(e))
bot.run(TOKEN)
    

"""
TODO
    - WRITE FUNCTION TO FETCH CARDS FROM DATABASE (Figure out exactly how I wanna do this, collectible vs non, show stats, include BG heros?, show golden img)
    - WRITE JSON PARSER FOR CARD METADATA
    - IMPROVE ERROR HANDLING
    - LOGGING DECORATOR
    - OPTIMIZATION
"""
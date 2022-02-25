import bot
from bot.bot import Bot, StartUpError
from .log import get_logger

try:
    bot.instance = Bot.create(command_prefix='!')
    bot.instance.initialize()
    bot.instance.run(bot.instance.token)
except StartUpError as e:
    logger = get_logger()
    logger.fatal(e.exception)

    exit(183)
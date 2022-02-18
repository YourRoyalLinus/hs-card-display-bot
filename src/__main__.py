import src
from src.bot import Bot, StartUpError
from .log import get_logger

try:
    src.instance = Bot.create(command_prefix='!')
    src.instance.initialize()
    src.instance.run(src.instance.token)
except StartUpError as e:
    logger = get_logger()
    logger.fatal(e.exception)

    exit(183)
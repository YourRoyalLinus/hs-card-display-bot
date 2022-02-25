from logging import Logger, Formatter, getLogger, handlers, INFO
from pathlib import Path

_BOT_LOGGER_NAME = 'hs-card-discord-bot'

def setup() -> None:
    """Set up the :class:`bot` Logger"""
    logger = getLogger(_BOT_LOGGER_NAME)
    logger.setLevel(INFO)
    
    log_file = Path("logs", "bot.log")
    log_file.parent.mkdir(exist_ok=True)
  
    formatter = Formatter('%(asctime)s - %(levelname)s - %(message)s', 
                            datefmt='%m/%d/%Y %H:%M:%S')
    file_handler = handlers.RotatingFileHandler(log_file, maxBytes=2097152,
                        backupCount=5, encoding="utf-8")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(INFO)

    logger.addHandler(file_handler)

    return None

def get_logger() -> Logger:
    """Return the logger for the bot. If this is the first call to get_logger,
    call log.setup to configure the logger
    
    Returns:
        logger.Logger(log._BOT_LOGGER_NAME)
    """
    logger_ =  getLogger(_BOT_LOGGER_NAME)

    if not logger_.hasHandlers():
        setup()

    return logger_


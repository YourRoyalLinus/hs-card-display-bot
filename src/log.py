import logging
import datetime

_LOGGING_DIR = r'./logs/'
_LOGGING_DATE = datetime.datetime.today().strftime('%Y%m%d')
_LOG_FILE = _LOGGING_DIR + 'LOG_' + _LOGGING_DATE + '.log'
_BOT_LOGGER_NAME = 'hs-card-discord-bot'

def _init() -> None:
    _LOGGER = logging.getLogger(_BOT_LOGGER_NAME)
    _LOGGER.setLevel(logging.INFO)
    formatter = logging.Formatter(
                        fmt='%(asctime)s - %(levelname)s - %(message)s', 
                        datefmt='%m/%d/%Y %H:%M:%S'
                        )
    fh = logging.FileHandler(_LOG_FILE, mode='a', encoding='utf-8')
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)

    _LOGGER.addHandler(fh)

    return None

def get_logger() -> logging.Logger:
    _logger =  logging.getLogger(_BOT_LOGGER_NAME)

    if not _logger.hasHandlers():
        _init()

    return _logger

